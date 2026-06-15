from pydantic import BaseModel, Field

class PermissionCreateRequest(BaseModel):

    name: str = Field(min_length=2, max_length=100)

    description: str = Field(min_length=5, max_length=255)

class PermissionResponse(BaseModel):

    id: int
    name: str
    description: str

    class Config:

        from_attributes = True