from typing import Optional, List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# 컬렉션에 넣을 틀 > 중복되지 않게 
'''
Python으로 작성된 코드로, FastAPI와 Beanie ODM를 사용하여 MongoDB와의 데이터 모델을 정의하는 예제입니다.
'''

class FinancialStatements(Document):
    name: str = None # None이라는거는 없어도 된다, str 으로 지정되어있는건 그런 형식을 지켜라
    email: Optional[str] = None # Optional str으로 권장하지만 아니어도 상관없고, None이라는거는 역시 없어도 된다
    roles :List[str] = ['MEMBER',] # List라고 하는
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
