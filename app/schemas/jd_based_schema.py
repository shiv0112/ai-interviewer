from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str | None = None
    job_desc: str | None = None
    message: str | None = None

class ChatResponse(BaseModel):
    session_id: str
    reply: str
