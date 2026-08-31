from pydantic import BaseModel, Field , EmailStr
from typing import Optional,Dict,Any
from datetime import datetime,date
from uuid import UUID

class LoginRequest(BaseModel):
    email : EmailStr = Field(... , examples=["deneme1@gmail.com"])
    password : str = Field(... , min_length=6 , examples=["Password123!"])

class TokenResponse(BaseModel):
    access_token: str
    refresh_token:str
    token_type:str = "bearer"
    expires_in:int
    user_id : UUID

class RefreshRequest(BaseModel):
    refresh_token:str

class RegisterRequest(BaseModel):
    email : EmailStr = Field(..., examples=["test@gmail.com"])
    password : str = Field(...,min_length=6,examples=["Password123!"])
    first_name : str = Field(... , min_length=2,examples=["Ömer"])
    last_name : str = Field(...,min_length=2,examples=["Gülşen"])
    nick_name : str | None = Field(min_length=3,default=None,examples=["omrfrk"])
    birth_date : date
    gender : str = Field(...,min_length=4,max_length=6,examples=["male"])
    avatar_url : str | None = None

class LoginResponse(TokenResponse):
    email : EmailStr
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)