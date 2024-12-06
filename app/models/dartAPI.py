from typing import Optional, List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class dartAPI(Document):
    CORP_CODE: str = None
    BUSINESS_YEAR: str = None
    FINANCIAL_STATEMENT_NAME :str = None
    CURRENT_TERM_AMOUNT: int = None
    PREVIOUS_TERM_AMOUNT: int = None
    BEFORE_PREVIOUS_TERM_AMOUNT: int = None
    # CREATED_AT: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_FINANCIAL_HISTORY"



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
