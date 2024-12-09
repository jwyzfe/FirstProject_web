from typing import Optional, List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class tossComments(Document):
    COMMENT: str = None
    DATE: str = None
    DATETIME :str = None
    SYMBOL: str = None
    UPDATED_AT: str = None
    CREATED_AT: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_SCRAPPING_TOSS_COMMENT_HISTORY"



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
