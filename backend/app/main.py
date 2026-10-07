import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ApplicationInput, AssessmentResponse
from app.services.nlp_pipeline import assess_application

app = FastAPI(title='Welfare Prioritization API', version='1.0.0')

allowed_origins = [
    origin.strip()
    for origin in os.getenv('WEB_ORIGIN', 'http://localhost:5173').split(',')
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def root():
    return {'message': 'Welfare Prioritization API is running'}


@app.post('/api/assess', response_model=AssessmentResponse)
def assess(payload: ApplicationInput):
    result = assess_application(payload.model_dump())
    return AssessmentResponse(**result)
