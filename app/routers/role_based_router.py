from fastapi import APIRouter, HTTPException
from app.models.role import RoleRequest
from app.chains.role_based_chain import get_role_based_chain
from app.utils.logger import logger

router = APIRouter(prefix="/generate/questions", tags=["Role-Based"])

@router.post("/role")
async def generate_questions_for_role(request: RoleRequest):
    try:
        logger.info(f"Generating questions for role: {request.role_name}")
        chain = get_role_based_chain()
        result = await chain.ainvoke({"role_name": request.role_name})
        questions = result.content if hasattr(result, "content") else str(result)
        return {"role": request.role_name, "questions": questions}

    except Exception as e:
        logger.error(f"Error generating role-based questions: {e}")
        raise HTTPException(status_code=500, detail="Error generating questions.")