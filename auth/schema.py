from fastapi import HTTPException , status
from pydantic import BaseModel, EmailStr, field_validator
import re

class User_create(BaseModel):
    username : str
    email : EmailStr
    password : str
    role : str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail="Password must be at least 8 characters")

        if not re.search(r"[A-Z]", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail="Password must contain uppercase letter")

        if not re.search(r"[0-9]", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail="Password must contain number")

        return value

class change_username(BaseModel):
    id : int
    username : str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT , detail="Password must be at least 8 characters")

        if not re.search(r"[A-Z]", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT , detail="Password must contain uppercase letter")

        if not re.search(r"[0-9]", value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT , detail="Password must contain number")

        return value