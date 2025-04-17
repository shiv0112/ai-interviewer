from pydantic import BaseModel, Field

class RoleRequest(BaseModel):
    role_name: str = Field(..., example="Data Scientist")