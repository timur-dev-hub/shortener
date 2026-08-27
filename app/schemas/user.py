from pydantic import BaseModel, ConfigDict
from pydantic import Field, EmailStr

from uuid import UUID

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

