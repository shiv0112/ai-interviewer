# resume_sessions.py
from typing import Dict
from uuid import uuid4

class ResumeSession:
    def __init__(self, resume_text: str):
        self.resume_text = resume_text
        self.chat_history: list[tuple[str, str]] = []
        self.chunk_usage: dict[str, int] = {}

_sessions: Dict[str, ResumeSession] = {}

def create_session(resume_text: str) -> str:
    session_id = str(uuid4())
    _sessions[session_id] = ResumeSession(resume_text)
    return session_id

def get_session(session_id: str) -> tuple[str, ResumeSession]:
    return session_id, _sessions[session_id]

def list_sessions():
    return [{ "session_id": sid, "messages": len(sess.chat_history)} for sid, sess in _sessions.items()]

def reset_session(session_id: str) -> bool:
    return _sessions.pop(session_id, None) is not None
