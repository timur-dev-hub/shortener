from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")


class LoginRegister(BaseModel):
    email: EmailStr
    password: str

