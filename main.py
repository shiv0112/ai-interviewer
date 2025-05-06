import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    status,
    role_based,
    jd,
    resume,
    hybrid,
)

app = FastAPI(
    title="AI Interviewer",
    description=(
        "A conversational mock-interview tool that adapts to your input—"
        "whether you supply a role title, a job description, your resume, or both. "
        "Powered by FastAPI, LangChain, and LLMs to generate targeted questions "
        "and follow-ups based on your background and the hiring criteria."
    ),
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
app.include_router(role_based.router)
app.include_router(jd.router)
app.include_router(resume.router)
app.include_router(hybrid.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
