from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Marketsenti(Document):
    DATE: datetime = Field(default_factory=datetime.now)
    MACD_HISTOGRAM: float = None
    MACD_LINE: float = None
    RSI : float = None
    SIGNAL_LINE : float = None
    TICKER : str = None
    CREATED_AT: datetime = Field(default_factory=datetime.now)
    

    class Settings:
        name = "COL_MARKETSENTI_HISTORY"



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
