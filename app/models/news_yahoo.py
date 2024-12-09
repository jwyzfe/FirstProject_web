from typing import Optional, List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field


class News_yahoo(Document):
    TITLE: str  # Optional 사용
    DATE: str
    NEWS_URL: str # 빈 리스트 기본값 설정
    CONTENTS: str   # Optional 사용
    CREATED_AT: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "COL_SCRAPPING_NEWS_YAHOO_HISTORY"  # collection 사용

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
