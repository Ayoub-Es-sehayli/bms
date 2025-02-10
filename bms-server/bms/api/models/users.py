from pydantic import BaseModel, Field, EmailStr

class UserCredentials(BaseModel):
    username: str = Field(title="User's email")
    password: str = Field(title="User's password")

class UserCreate(BaseModel):
    username: str = Field(title="User's username for Authentication")
    email: EmailStr = Field(title="User's email")
    name: str = Field(title="User's name")

class LoginResponse(UserCreate):
    token: str = Field(title="Hashed access token")

class LoginFailedResponse(BaseModel):
    message: str = Field(title="Failure message")
