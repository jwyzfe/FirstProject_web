from typing import Optional, List
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field

class PriceData(BaseModel):
    OPEN: float = None
    HIGH: float = None
    LOW: float = None
    CLOSE: float = None
    VOLUME: int = None
    STOCKSPLITS: float = Field(default=0)
    DIVIDENDS: float = Field(default=0)

class TimeData(BaseModel):
    DATE: datetime = Field(default_factory=datetime.now)
    PRICE_DATA: PriceData

class Stockprice(Document):
    SYMBOL: str = None
    TIME_DATA: TimeData
    CREATED_AT: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "COL_STOCKPRICE_EMBEDDED"

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
