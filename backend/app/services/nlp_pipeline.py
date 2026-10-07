import re
from typing import Dict, List, Tuple

URGENCY_HIGH = [
    'urgent', 'immediately', 'critical', 'dying', 'emergency', 'severe',
    'cannot afford', 'life threatening', 'no food', 'homeless', 'evicted',
    'hospital', 'surgery', 'cancer', 'dialysis', 'zaroor', 'mushkil',
    'khatarnak', 'bohot bura', 'shiddat'
]
URGENCY_MEDIUM = [
    'struggling', 'difficult', 'need', 'require', 'support', 'help',
    'problem', 'issue', 'concern', 'limited', 'insufficient', 'zaroorat',
    'chahiye', 'imdaad', 'madad', 'mushkil'
]
URGENCY_LOW = [
    'would like', 'hoping', 'prefer', 'interested', 'considering',
    'enhance', 'improve', 'better', 'opportunity'
]

KEYWORD_MAP = {
    'Medical': ['ill', 'sick', 'disease', 'medical', 'treatment', 'hospital', 'doctor',
                'cancer', 'diagnosed', 'medicine', 'dialysis', 'chemo', 'tilaaj', 'sehat'],
    'Education': ['school', 'education', 'fees', 'fee', 'tuition', 'college', 'university',
                  'study', 'admission', 'student', 'parhai', 'bachay'],
    'Food': ['food', 'hungry', 'ration', 'meal', 'grain', 'khana', 'eat', 'starving', 'shortage'],
    'Housing': ['rent', 'house', 'shelter', 'roof', 'evict', 'makaan', 'kiraya', 'housing', 'flood'],
    'Utility': ['electricity', 'gas', 'bill', 'water', 'utility', 'bijli', 'connection', 'power', 'overdue']
}

WEIGHTS = {
    'income': 0.35,
    'dependents': 0.20,
    'urgency': 0.20,
    'employment': 0.10,
    'hh_size': 0.10,
    'dup_penalty': 0.05,
}

URGENCY_MAP = {'High': 1.0, 'Medium': 0.5, 'Low': 0.1}
EMPLOYMENT_MAP = {'Unemployed': 1.0, 'Part-time': 0.7, 'Self-employed': 0.4, 'Full-time': 0.1}


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())


def predict_category(text: str) -> str:
    text_lower = preprocess_text(text)
    scores = {category: sum(1 for kw in kws if kw in text_lower) for category, kws in KEYWORD_MAP.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'Others'


def score_urgency(text: str) -> Tuple[str, int]:
    lower = preprocess_text(text)
    h = sum(1 for kw in URGENCY_HIGH if kw in lower)
    m = sum(1 for kw in URGENCY_MEDIUM if kw in lower)
    l = sum(1 for kw in URGENCY_LOW if kw in lower)
    score = h * 3 + m * 1 - l * 1
    if score >= 3:
        return 'High', score
    if score >= 1:
        return 'Medium', score
    return 'Low', score


def normalize_income(income: float, max_income: float = 100000.0) -> float:
    capped = min(income, max_income)
    return 1.0 - (capped / max_income) if max_income > 0 else 0.0


def compute_cds(applicant: Dict[str, float]) -> Dict[str, object]:
    income = float(applicant.get('income', 0) or 0)
    dependents = int(applicant.get('number_of_dependents', 0) or 0)
    household_size = int(applicant.get('household_size', 1) or 1)
    urgency_level = applicant.get('urgency_level', 'Medium')
    employment_status = applicant.get('employment_status', 'Unemployed')
    duplicate_flag = bool(applicant.get('duplicate_flag', False))

    income_score = normalize_income(income, 100000.0)
    dep_score = dependents / max(1, 10)
    hh_score = household_size / max(1, 10)
    urgency_score = URGENCY_MAP.get(urgency_level, 0.5)
    employ_score = EMPLOYMENT_MAP.get(employment_status, 0.3)
    dup_penalty = 1.0 if duplicate_flag else 0.0

    raw = (
        WEIGHTS['income'] * income_score +
        WEIGHTS['dependents'] * dep_score +
        WEIGHTS['urgency'] * urgency_score +
        WEIGHTS['employment'] * employ_score +
        WEIGHTS['hh_size'] * hh_score
    )
    cds = (raw - WEIGHTS['dup_penalty'] * dup_penalty) * 100
    final_cds = round(max(0, min(100, cds)), 2)

    breakdown = {
        'income': round(WEIGHTS['income'] * income_score * 100, 2),
        'dependents': round(WEIGHTS['dependents'] * dep_score * 100, 2),
        'urgency': round(WEIGHTS['urgency'] * urgency_score * 100, 2),
        'employment': round(WEIGHTS['employment'] * employ_score * 100, 2),
        'household_size': round(WEIGHTS['hh_size'] * hh_score * 100, 2),
        'duplicate_penalty': round(-WEIGHTS['dup_penalty'] * dup_penalty * 100, 2),
    }

    return {
        'cds': final_cds,
        'breakdown': breakdown,
    }


def assess_application(applicant: Dict[str, object]) -> Dict[str, object]:
    narrative = str(applicant.get('narrative', ''))
    category = predict_category(narrative)
    urgency_level, urgency_score = score_urgency(narrative)
    duplicate_flag = False

    score_data = {
        'income': float(applicant.get('income', 0) or 0),
        'number_of_dependents': int(applicant.get('number_of_dependents', 0) or 0),
        'household_size': int(applicant.get('household_size', 1) or 1),
        'urgency_level': urgency_level,
        'employment_status': str(applicant.get('employment_status', 'Unemployed')),
        'duplicate_flag': duplicate_flag,
    }
    cds_result = compute_cds(score_data)

    explanation = (
        f"Need category: {category}. Urgency: {urgency_level}. "
        f"Composite Deserving Score: {cds_result['cds']} / 100 based on income, dependents, urgency, employment, and household size."
    )

    return {
        'need_category': category,
        'urgency_level': urgency_level,
        'urgency_score': urgency_score,
        'duplicate_flag': duplicate_flag,
        'cds': cds_result['cds'],
        'breakdown': cds_result['breakdown'],
        'explanation': explanation,
    }
