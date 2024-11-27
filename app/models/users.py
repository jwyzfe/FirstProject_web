from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(Document):
    name: str = None
    email: Optional[str] = None
    roles :List[str] = ['MEMBER',]
    create_date: datetime = Field(default_factory=datetime.now)
    last_access_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
