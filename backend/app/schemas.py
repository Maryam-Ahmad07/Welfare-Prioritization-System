from pydantic import BaseModel, Field
from typing import Optional, Dict


class ApplicationInput(BaseModel):
    narrative: str = Field(..., min_length=10)
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., ge=0)
    number_of_dependents: int = Field(..., ge=0)
    household_size: int = Field(..., ge=1)
    employment_status: str = Field(default="Unemployed")
    location: str = Field(default="Urban")
    gender: str = Field(default="Male")
    applicant_id: Optional[str] = None


class AssessmentResponse(BaseModel):
    need_category: str
    urgency_level: str
    urgency_score: int
    duplicate_flag: bool
    cds: float
    breakdown: Dict[str, float]
    explanation: str
