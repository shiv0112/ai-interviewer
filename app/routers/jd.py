from fastapi import APIRouter, HTTPException
from app.schemas.jd_based_schema import ChatRequest, ChatResponse
from app.memory.jd_sessions import get_session, list_sessions, reset_session
from app.chains.jd_based_chain import get_role_conversation_chain, get_evaluation_chain
from app.utils.logger import logger

router = APIRouter(prefix="/chat/jd", tags=["JD-Based-Chat"])

@router.get("/sessions")
def get_all_sessions():
    """
    Returns all active session IDs with their role name and message count.
    """
    sessions = list_sessions()
    return {"active_sessions": sessions}

@router.post("/reset")
def reset_chat_session(session_id: str):
    """
    Reset the conversation session by session_id.
    Clears memory and deletes session.
    """
    was_reset = reset_session(session_id)
    if was_reset:
        return {"status": "success", "message": f"Session {session_id} reset successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session ID not found")

@router.post("/interview", response_model=ChatResponse)
async def interview_jd(req: ChatRequest):
    """
    Stateful jd-based conversation using ConversationBufferMemory.
    The first message should include `job_desc` without `session_id`.
    All following messages should include `session_id` and `message`.
    """
    # Case 1: New session → job_desc required
    if not req.session_id:
        if not req.job_desc:
            raise HTTPException(400, "Missing job_desc for new conversation.")

        sid, session = get_session(None)
        session.job_desc = req.job_desc.strip()

        chain = get_role_conversation_chain(session.memory, session.job_desc)
        try:
            bot_reply = await chain.apredict(
                input="Hi, I'm ready to begin for my interview."
            )
        except Exception as e:
            logger.error(f"[RoleChatError][sid={sid}][first]: {e}")
            raise HTTPException(500, "Failed to start role-based interview.")
        
        return ChatResponse(session_id=sid, reply=bot_reply)

    # Case 2: Existing session → job_desc from memory + message
    else:
        if not req.message:
            raise HTTPException(400, "Missing message for continued conversation.")

        sid, session = get_session(req.session_id)
        if not session.job_desc:
            raise HTTPException(400, "job_desc missing in session.")

        chain = get_role_conversation_chain(session.memory, session.job_desc)
        try:
            bot_reply = await chain.apredict(
                input=req.message
            )
        except Exception as e:
            logger.error(f"[RoleChatError][sid={sid}][continue]: {e}")
            raise HTTPException(500, "Failed to continue role-based interview.")
        
        return ChatResponse(session_id=sid, reply=bot_reply)
    
@router.post("/evaluate")
async def evaluate_candidate(session_id: str):
    """
    Evaluates the entire chat session and provides an overall feedback summary.
    """
    sid, session = get_session(session_id)

    if not session.job_desc:
        raise HTTPException(400, "job_desc is missing for the session")

    chat_log = session.memory.load_memory_variables({})
    chat_history = chat_log.get("chat_history", "")

    chain = get_evaluation_chain()

    try:
        result = await chain.ainvoke({
            "job_desc": session.job_desc,
            "chat_history": chat_history
        })

        feedback = result.content if hasattr(result, "content") else str(result)

        return {
            "session_id": sid,
            "feedback": feedback
        }
    
    except Exception as e:
        logger.error(f"[EvaluationError][sid={sid}]: {e}")
        raise HTTPException(500, "Failed to evaluate session.")