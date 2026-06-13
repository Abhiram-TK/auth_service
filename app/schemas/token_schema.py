from pydantic import BaseModel

class TokenValidationRequest(BaseModel):

    token: str