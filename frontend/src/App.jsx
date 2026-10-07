import { useState } from 'react'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

const initialForm = {
  narrative: 'My household is struggling to pay rent and buy food. I have three dependents and my income is low. Please help with urgent support.',
  age: 42,
  income: 35000,
  number_of_dependents: 3,
  household_size: 5,
  employment_status: 'Unemployed',
  location: 'Urban',
  gender: 'Male'
}

const emptyResult = {
  need_category: '',
  urgency_level: '',
  urgency_score: 0,
  duplicate_flag: false,
  cds: 0,
  breakdown: {},
  explanation: ''
}

function App() {
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(emptyResult)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_URL}/api/assess`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...form,
          income: Number(form.income),
          age: Number(form.age),
          number_of_dependents: Number(form.number_of_dependents),
          household_size: Number(form.household_size)
        })
      })

      if (!response.ok) {
        throw new Error('Request failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Unable to connect to the backend API. Start FastAPI first.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Welfare Prioritization</p>
          <h1>Applicant Assessment Dashboard</h1>
        </div>
      </header>

      <main className="layout">
        <form className="panel" onSubmit={handleSubmit}>
          <h2>Applicant Details</h2>

          <label>
            Narrative
            <textarea
              name="narrative"
              value={form.narrative}
              onChange={handleChange}
              rows={5}
            />
          </label>

          <div className="grid-2">
            <label>
              Age
              <input name="age" type="number" value={form.age} onChange={handleChange} />
            </label>

            <label>
              Income
              <input name="income" type="number" value={form.income} onChange={handleChange} />
            </label>

            <label>
              Dependents
              <input name="number_of_dependents" type="number" value={form.number_of_dependents} onChange={handleChange} />
            </label>

            <label>
              Household Size
              <input name="household_size" type="number" value={form.household_size} onChange={handleChange} />
            </label>
          </div>

          <div className="grid-2">
            <label>
              Employment Status
              <select name="employment_status" value={form.employment_status} onChange={handleChange}>
                <option>Unemployed</option>
                <option>Part-time</option>
                <option>Self-employed</option>
                <option>Full-time</option>
              </select>
            </label>

            <label>
              Location
              <select name="location" value={form.location} onChange={handleChange}>
                <option>Urban</option>
                <option>Rural</option>
                <option>Suburban</option>
              </select>
            </label>

            <label>
              Gender
              <select name="gender" value={form.gender} onChange={handleChange}>
                <option>Male</option>
                <option>Female</option>
              </select>
            </label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Assessing...' : 'Assess Application'}
          </button>
          {error && <p className="error">{error}</p>}
        </form>

        <aside className="panel result-panel">
          <h2>Assessment Result</h2>

          {result.need_category ? (
            <>
              <div className="badge-row">
                <span className="badge">Category: {result.need_category}</span>
                <span className="badge badge-alt">Urgency: {result.urgency_level}</span>
              </div>

              <div className="score-box">
                <div className="score-label">CDS Score</div>
                <div className="score-value">{result.cds}</div>
              </div>

              <div className="meta-list">
                <p><strong>Duplicate Flag:</strong> {result.duplicate_flag ? 'Yes' : 'No'}</p>
                <p><strong>Urgency Score:</strong> {result.urgency_score}</p>
              </div>

              <div className="breakdown">
                <h3>Score Breakdown</h3>
                {Object.entries(result.breakdown).map(([k, v]) => (
                  <div className="row" key={k}>
                    <span>{k}</span>
                    <strong>{v}</strong>
                  </div>
                ))}
              </div>

              <p className="explanation">{result.explanation}</p>
            </>
          ) : (
            <p className="placeholder">Submit an application to see prioritized results.</p>
          )}
        </aside>
      </main>
    </div>
  )
}

export default App
