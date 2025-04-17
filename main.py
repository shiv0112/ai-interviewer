import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    status,
    role_based_router,
    feedback_router, 
    resume_jd_router, 
)

app = FastAPI(
    title="AI Interviewer",
    description="AI Interviewer to prepare for interviews using the Resume and Job Description, or in general to prepare for any job interview",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers correctly
app.include_router(status.router)
app.include_router(role_based_router.router)
# app.include_router(feedback_router.router)
# app.include_router(resume_jd_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
