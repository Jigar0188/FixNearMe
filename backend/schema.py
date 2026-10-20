
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: Annotated[str, Field(...,min_length=2, max_length=100, description="Enter your name")]
    email: Annotated[EmailStr, Field(..., description="Enter your email address")]
    password: Annotated[str, Field(...,min_length=8, max_length=128,description="Password")]
    role: Literal["customer", "professional"]
    phone: Annotated[str | None, Field(default=None, max_length=20)]   


class RegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)
    


class CurrentUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)
