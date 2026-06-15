from pydantic import BaseModel
from typing import Literal

class UserResponse(BaseModel):

    id: int
    email: str
    username: str
    role: str
    is_active: bool

    class Config:

        from_attributes = True

class RoleUpdateRequest(BaseModel):

    role: Literal["viewer", "recruiter", "admin"]