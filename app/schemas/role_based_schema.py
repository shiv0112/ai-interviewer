from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str | None = None
    role_name: str | None = None
    message: str | None = None

class ChatResponse(BaseModel):
    session_id: str
    reply: str
