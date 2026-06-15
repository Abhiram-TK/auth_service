from pydantic import BaseModel, Field

class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    role: str
    is_active: bool

    class Config:

        from_attributes = True

class RoleUpdateRequest(BaseModel):

    role: str = Field(min_length=2, max_length=50)