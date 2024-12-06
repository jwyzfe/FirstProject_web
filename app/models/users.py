from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# class User(Document):
#     name: str = None #id nosql 담겨있는 형식으로 작성
#     email: Optional[str] = None
#     roles :List[str] = ['MEMBER',]
#     create_date: datetime = Field(default_factory=datetime.now)
#     last_access_date: datetime = Field(default_factory=datetime.now)

#     class Settings:
#         name = "users"

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!"
#             }
#         }


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str

''' 기사클릭시 내용을 어떻게 구현(?) 나타낼지? '''

class Hankyung(Document):
    CONTENTS: str
    CREATED_AT: datetime = Field(default_factory=datetime.now) # 자동으로 현재 시간
    DATE: str
    LINK: str
    TITLE: str
    

class Settings:
    name = "COL_SCRAPPING_HANKYUNG_HISTORY"

