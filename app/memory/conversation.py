from uuid import uuid4
from langchain.memory import ConversationBufferMemory

class ChatSession:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.role_name: str | None = None

_sessions: dict[str, ChatSession] = {}

def get_session(session_id: str | None) -> tuple[str, ChatSession]:
    if not session_id or session_id not in _sessions:
        session_id = str(uuid4())
        _sessions[session_id] = ChatSession()
    return session_id, _sessions[session_id]
