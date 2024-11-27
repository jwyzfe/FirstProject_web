from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Stockprice(Document):
    SYMBOL: str = None
    CLOSE: float = None
    VOLUME: int = None
    # roles :List[str] = ['MEMBER',]
    CREATED_AT: datetime = Field(default_factory=datetime.now)
    # last_access_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_STOCKPRICE_DAILY"

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
