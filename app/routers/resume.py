import os
import tempfile
import traceback
from datetime import datetime, timedelta
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_loader import load_pdf
from app.chains.resume_based_chain import (
    build_resume_chain, get_evaluation_chain, ingest_documents, delete_old_sessions
)
from app.memory.resume_sessions import create_session, get_session, list_sessions, reset_session
from app.schemas.resume_based_schema import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat/resume-rag", tags=["Resume-Based"])

@router.get("/sessions")
def get_all_sessions():
    return {"active_sessions": list_sessions()}

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            temp_file.write(await file.read())

        docs = load_pdf(temp_path)
        os.remove(temp_path)

        resume_text = docs[0].page_content
        session_id = create_session(resume_text=resume_text)

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
async def resume_interview(req: ChatRequest):
    if not req.session_id or not req.message:
        raise HTTPException(status_code=400, detail="Missing session_id or message.")

    try:
        try:
            _, session = get_session(req.session_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Session not found.")

        resume_chain = build_resume_chain(req.session_id)

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

        response = resume_chain.invoke({
            "input": final_input,
            "chat_history": chat_history
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

        eval_chain = get_evaluation_chain()
        result = await eval_chain.apredict({
            "resume": session.resume_text,
            "chat_history": chat_history
        })

        return {
            "session_id": session_id,
            "feedback": result if isinstance(result, str) else getattr(result, "content", str(result))
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")

@router.post("/reset")
def reset_resume_session(session_id: str):
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