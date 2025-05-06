# hybrid_session.py

from typing import Dict
from uuid import uuid4

class HybridSession:
    def __init__(self, resume_text: str, jd_or_role: str):
        self.resume_text = resume_text
        self.jd_or_role =  jd_or_role
        self.chat_history: list[tuple[str, str]] = []
        self.chunk_usage: dict[str, int] = {}

_sessions: Dict[str, HybridSession] = {}

def create_session(resume_text: str, jd_or_role: str) -> str:
    session_id = str(uuid4())
    _sessions[session_id] = HybridSession(resume_text, jd_or_role)
    return session_id

def get_session(session_id: str) -> tuple[str, HybridSession]:
    return session_id, _sessions[session_id]

def list_sessions():
    return [{ "session_id": sid, "messages": len(sess.chat_history)} for sid, sess in _sessions.items()]

def reset_session(session_id: str) -> bool:
    return _sessions.pop(session_id, None) is not None
