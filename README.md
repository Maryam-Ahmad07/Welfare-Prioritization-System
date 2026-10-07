# Welfare Prioritization Full-Stack Starter

This project is a starter implementation of the React + FastAPI architecture for the welfare prioritization system.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- NLP / scoring logic: Python utilities

## Project structure

```bash
welfare_prioritization_app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services/
│   │       └── nlp_pipeline.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── README.md
└── .gitignore
```

## Run backend

```bash
cd backend
py -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Run frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Then open:

- Frontend: http://localhost:5173/
- API: http://localhost:8000/

## API endpoint

POST /api/assess

Example body:

```json
{
  "narrative": "My household is struggling to pay rent and buy food. I have three dependents and my income is low.",
  "age": 42,
  "income": 35000,
  "number_of_dependents": 3,
  "household_size": 5,
  "employment_status": "Unemployed",
  "location": "Urban",
  "gender": "Male"
}
```

## Deploy frontend and backend separately

This setup uses Render for the FastAPI backend and Vercel for the React frontend.

### 1. Deploy the backend to Render

1. Push this project to a GitHub repository.
2. In Render, create a **Blueprint** from that repository. Render will use the root `render.yaml` to build and start the API.
3. Copy the deployed service URL, such as `https://welfare-prioritization-api.onrender.com`.

### 2. Deploy the frontend to Vercel

1. In Vercel, import the same GitHub repository.
2. Set the **Root Directory** to `frontend`.
3. Set the build command to `npm run build` and the output directory to `dist`.
4. Add the environment variable `VITE_API_URL` with the Render backend URL (no trailing slash), then deploy.
5. Copy the deployed frontend origin, such as `https://your-project.vercel.app`.

### 3. Allow the deployed frontend to call the API

In Render, open the backend service's environment settings and set `WEB_ORIGIN` to the Vercel frontend origin. For multiple frontend origins, separate them with commas. Save the setting so Render redeploys the backend.

Test the backend at its `/` URL and submit an assessment in the deployed frontend. If you later change the Vercel domain, update `WEB_ORIGIN` in Render to match.

## Notes

This is a starter integration built on top of the rule-based prioritization logic and is ready to be connected to a trained ML model or database in the next phase.
