from pydantic import BaseModel

class UserResponse(BaseModel):

    id: int
    email: str
    username: str
    role: str
    is_active: bool

    class Config:

        from_attributes = True

class RoleUpdateRequest(BaseModel):

    role: str