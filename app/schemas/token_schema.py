from pydantic import BaseModel, Field

class TokenValidationRequest(BaseModel):

    token: str = Field(...,
                       description="Complete JWT access token returned by POST /login.")