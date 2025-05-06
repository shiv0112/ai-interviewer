import os
import tempfile
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_loader import load_pdf
from app.chains.hybrid_chain import (
    build_hybrid_chain, get_evaluation_chain, ingest_documents, delete_old_sessions
)
from app.memory.hybrid_sessions import create_session, get_session, list_sessions, reset_session
from app.schemas.hybrid_schema import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat/hybrid-rag", tags=["Hybrid-Mode"])

@router.get("/sessions")
def get_all_sessions():
    return {"active_sessions": list_sessions()}

@router.post("/upload")
async def upload_resume_and_job_details(file: UploadFile = File(...), jd_or_role: str = None):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    if not jd_or_role:
        raise HTTPException(status_code=400, detail="Job details (jd_or_role) are missing.")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            temp_file.write(await file.read())

        docs = load_pdf(temp_path)
        os.remove(temp_path)

        resume_text = docs[0].page_content
        session_id = create_session(resume_text=resume_text, jd_or_role=jd_or_role)

        ingest_documents(session_id, docs)

        return {
            "status": "success",
            "session_id": session_id,
            "message": "Resume uploaded and session created."
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Resume upload failed: {str(e)}")

@router.post("/interview", response_model=ChatResponse)
async def start_interview(req: ChatRequest):
    if not req.session_id or not req.message:
        raise HTTPException(status_code=400, detail="Missing session_id or message.")

    try:
        try:
            _, session = get_session(req.session_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Session not found.")

        hybrid_chain = build_hybrid_chain(req.session_id)

        is_first_message = len(session.chat_history) == 0

        if is_first_message:
            chat_instruction = (
                "This is the first message from the candidate. "
                "Politely acknowledge the message, and then begin the interview by asking a relevant, ask the user to introduce themselves or ask them about their experience. "
                "Do not be generic."
            )
            final_input = f"{req.message}\n\n{chat_instruction}"
        else:
            final_input = req.message

        chat_lines = [f"User: {q}\nAI: {a}" for q, a in session.chat_history]
        chat_history = "\n\n".join(chat_lines)

        response = hybrid_chain.invoke({
            "input": final_input,
            "chat_history": chat_history,
            "jd_or_role": session.jd_or_role
             })
        
        reply = response if isinstance(response, str) else response.get("answer", str(response))

        print("Reply:", reply)

        session.chat_history.append((req.message, reply))
        return ChatResponse(session_id=req.session_id, reply=reply)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Resume chat error: {str(e)}")

@router.post("/evaluate")
async def evaluate_candidate(session_id: str):
    try:
        try:
            _, session = get_session(session_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Session not found.")

        if not session.resume_text:
            raise HTTPException(400, "Resume text is missing in session.")

        chat_lines = [f"User: {q}\nAI: {a}" for q, a in session.chat_history]
        chat_history = "\n\n".join(chat_lines)

        chain = get_evaluation_chain()

        result = await chain.ainvoke({
            "resume": session.resume_text,
            "chat_history": chat_history,
            "jd_or_role": session.jd_or_role
        })

        feedback = result.content if hasattr(result, "content") else str(result)

        return {
            "session_id": session_id,
            "feedback": feedback
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")

@router.post("/reset")
def reset_hybrid_session(session_id: str):
    if reset_session(session_id):
        return {"status": "success", "message": f"Session {session_id} deleted."}
    else:
        raise HTTPException(status_code=404, detail="Session ID not found.")

@router.post("/cleanup-old-sessions")
def cleanup_old_sessions(mins: int = 30):
    try:
        delete_old_sessions(mins=mins)
        return {"status": "success", "message": f"Sessions older than {mins} mins cleaned up."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")