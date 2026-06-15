from pydantic import BaseModel, Field

class RoleCreateRequest(BaseModel):

    name: str = Field(min_length=3, max_length=50)

    description: str = Field(min_length=5, max_length=255)

class RoleResponse(BaseModel):

    id: int
    name: str
    description: str

    class Config:

        from_attributes = True