from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Stockprice(Document):
    symbol: str = None
    Close: float = None
    Volume: int = None
    # roles :List[str] = ['MEMBER',]
    created_at: datetime = Field(default_factory=datetime.now)
    # last_access_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_STOCKPRICE_HISTORY"

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "email": "fastapi@packt.com",
    #             "password": "strong!!!"
    #         }
    #     }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
