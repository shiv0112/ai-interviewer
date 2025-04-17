from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter()

@router.get("/", summary="Live Check", description="Returns the live status of the API.")
async def status_check():
    logger.info("Live status requested.")
    return {"message": "🤖 AI Interviewer is up and running!"}
