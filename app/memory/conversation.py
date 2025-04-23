from uuid import uuid4
from datetime import datetime, timedelta
from langchain.memory import ConversationBufferMemory

SESSION_TIMEOUT_MINUTES = 20  # Auto-expire sessions after 20 minutes of inactivity

class ChatSession:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.role_name: str | None = None
        self.created_at = datetime.utcnow()
        self.last_accessed = datetime.utcnow()

_sessions: dict[str, ChatSession] = {}

def get_session(session_id: str | None) -> tuple[str, ChatSession]:
    now = datetime.utcnow()

    # Step 1: Clean up expired sessions
    expired_ids = [
        sid for sid, session in _sessions.items()
        if now - session.last_accessed > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    ]
    for sid in expired_ids:
        del _sessions[sid]

    # Step 2: Create or retrieve session
    if not session_id or session_id not in _sessions:
        session_id = str(uuid4())
        _sessions[session_id] = ChatSession()

    # Step 3: Update last accessed time
    _sessions[session_id].last_accessed = now

    return session_id, _sessions[session_id]

def reset_session(session_id: str) -> bool:
    """
    Delete session memory for the given session_id.
    Returns True if session existed and was deleted.
    """
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False

def list_sessions() -> list[dict]:
    """
    Returns a list of all active sessions with basic info.
    """
    sessions_summary = []
    for session_id, session in _sessions.items():
        chat_log = session.memory.load_memory_variables({})
        chat_history = chat_log.get("chat_history", "")
        message_count = chat_history.count("Human:")

        sessions_summary.append({
            "session_id": session_id,
            "role_name": session.role_name,
            "message_count": message_count,
            "created_at": session.created_at.isoformat(),
            "last_accessed": session.last_accessed.isoformat(),
        })

    return sessions_summary
