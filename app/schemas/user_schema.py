from pydantic import BaseModel, ConfigDict, Field

class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class RoleUpdateRequest(BaseModel):

    role: str = Field(min_length=2, max_length=50)