from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Stocktwits(Document):
    SYMBOL: str = None
    CONTENT: str = None
    DATETIME: str = None
    LINKS : List[str] = ['MEMBER',]
    CREATED_AT: datetime = Field(default_factory=datetime.now)
    # last_access_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_SCRAPPING_STOCKTWITS_COMMENT_DAILY"

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
