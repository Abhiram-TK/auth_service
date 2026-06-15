from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)