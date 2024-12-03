from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from app.models.users import User
from app.models.stockprice import Stockprice
from app.models.stocktwits import Stocktwits

import os
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[User, Stockprice, Stocktwits])

    class Config:
        env_file = os.path.join("app",".env")

from app.utils.paginations import Paginations

import json
class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document):
        result = await document.create()
        return result

    async def get(self, id: PydanticObjectId):
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self, conditions: dict = {}):
        docs = await self.model.find_all(conditions).to_list()
        return docs

    # update with params json
    async def update_withjson(self, id: PydanticObjectId, body: json):
        doc_id = id

        # des_body = {k: v for k, v in des_body.items() if v is not None}
        # update_query = {"$set": {**body}}
        update_query = body

        doc = await self.get(doc_id)
        if not doc:
            return False
        update_doc = await doc.update(update_query)
        return update_doc
    
    async def update(self, id: PydanticObjectId, body: BaseModel):
        doc_id = id
        if hasattr(body, 'dict'):
            des_body = body.dict()
        else:
            des_body = body
            
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        update_doc = await doc.update(update_query)
        return update_doc

    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    # column 값으로 Documents 가져오기
    async def getbyconditions(self, conditions:dict = {}) -> [Any]:
        document = await self.model.find_one(conditions)  # find({})
        return document    

    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict = {}) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        return documents    

    # column 값으로 여러 Documents 가져오기
    async def getcountbyconditions(self, conditions:dict = {}) -> [Any]:
        try:
            count = await self.model.find(conditions).count()  # find({})
        except:
            count = 0

        return count    

    # column 값으로 aggregate해 여러 Documents 가져오기
    async def aggregatebyconditions(self, conditions:list) -> [Any]:
        documents = await self.model.aggregate(conditions).to_list()  # find({})
        return documents    

    async def aggregatebyconditionswithpagination(self, conditions: dict, page_number=1, records_per_page=10, pages_per_block=5, sorted='-', sort_field='create_date'):
        total = 0
        try:
            # Ensure conditions are in the right format
            if not isinstance(conditions, list):
                conditions = [{'$match': conditions}]
            
            # Get the total count of documents matching the conditions
            total = await self.model.aggregate(conditions + [{'$count': 'count'}]).to_list()
            total = total[0]['count'] if total else 0
            
            pagination = Paginations(total_records=total, current_page=page_number,
                                    records_per_page=records_per_page,
                                    pages_per_block=pages_per_block)
            
            # Get documents with sorting and pagination
            documents = await self.model.aggregate(
                conditions +
                [{'$sort': {sort_field: 1 if sorted == '+' else -1}},
                {'$skip': pagination.start_record_number},
                {'$limit': pagination.records_per_page}]
            ).to_list()

            return documents, pagination

        except Exception as e:
            # Log the error for debugging
            print(f"Error in aggregatebyconditionswithpagination: {e}")
            pagination = Paginations(total_records=total, current_page=page_number,
                        records_per_page=records_per_page,
                        pages_per_block=pages_per_block)


            return [], pagination

    # column 값으로 여러 Documents with pagination 가져오기
    async def getsbyconditionswithpagination(self
                                             , conditions:dict, page_number=1
                                             , records_per_page=10, pages_per_block=5
                                             , sorted = '-'
                                             , sort_field:str = 'CREATED_AT') -> [Any]:
        try:
            total = await self.model.find(conditions).count()
        except:
            total = 0
        pagination = Paginations(total_records=total, current_page=page_number
                                 , records_per_page=records_per_page
                                 , pages_per_block=pages_per_block)
        documents = await self.model.find(conditions).sort(f'{sorted}{sort_field}').skip(pagination.start_record_number).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return [], pagination     
    
    async def get_symbol_summary_with_pagination(self
                                            , conditions: dict = {}
                                            , page_number=1
                                            , records_per_page=10
                                            , pages_per_block=5) -> [Any]:
        try:
            # 심볼별 요약 정보를 가져오는 파이프라인 (단순화)
            pipeline = [
                {"$match": conditions},
                {"$group": {
                    "_id": "$SYMBOL",
                    "created_at": {"$first": "$CREATED_AT"}
                }},
                {"$sort": {"_id": 1}},
                {"$skip": (page_number - 1) * records_per_page},
                {"$limit": records_per_page},
                {"$project": {
                    "_id": 1,
                    "SYMBOL": "$_id",
                    "CREATED_AT": "$created_at"
                }}
            ]
            
            # 전체 심볼 수 계산을 위한 파이프라인
            count_pipeline = [
                {"$match": conditions},
                {"$group": {
                    "_id": "$SYMBOL"
                }},
                {"$count": "total"}
            ]
            
            # 병렬 실행
            data_future = self.model.aggregate(pipeline).to_list()
            total_future = self.model.aggregate(count_pipeline).to_list()
            
            data = await data_future
            total_result = await total_future
            
            total = total_result[0]["total"] if total_result else 0
            
            pagination = Paginations(total_records=total
                                , current_page=page_number
                                , records_per_page=records_per_page
                                , pages_per_block=pages_per_block)
            
            return data, pagination
            
        except Exception as e:
            print(f"Error in get_symbol_summary_with_pagination: {e}")
            return [], Paginations(total_records=0
                                , current_page=page_number
                                , records_per_page=records_per_page
                                , pages_per_block=pages_per_block), []

    async def get_symbol_prices(self, symbol: str, start_date=None, end_date=None) -> [Any]:
        try:
            # 기본 조건
            conditions = {"SYMBOL": symbol}
            
            # 날짜 조건 추가
            if start_date or end_date:
                date_condition = {}
                if start_date:
                    date_condition["$gte"] = start_date
                if end_date:
                    date_condition["$lte"] = end_date
                if date_condition:
                    conditions["TIME_DATA.DATE"] = date_condition

            # 데이터 조회 및 변환
            documents = await self.model.find(conditions).sort("+TIME_DATA.DATE").to_list()
            
            # 임베디드 구조를 평탄화하여 반환
            transformed_docs = []
            for doc in documents:
                transformed_doc = {
                    "_id": doc.id,
                    "SYMBOL": doc.SYMBOL,
                    "DATE": doc.TIME_DATA.DATE,
                    "OPEN": doc.TIME_DATA.PRICE_DATA.OPEN,
                    "HIGH": doc.TIME_DATA.PRICE_DATA.HIGH,
                    "LOW": doc.TIME_DATA.PRICE_DATA.LOW,
                    "CLOSE": doc.TIME_DATA.PRICE_DATA.CLOSE,
                    "VOLUME": doc.TIME_DATA.PRICE_DATA.VOLUME,
                    "STOCKSPLITS": doc.TIME_DATA.PRICE_DATA.STOCKSPLITS,
                    "DIVIDENDS": doc.TIME_DATA.PRICE_DATA.DIVIDENDS,
                    "CREATED_AT": doc.CREATED_AT
                }
                transformed_docs.append(transformed_doc)
                
            return transformed_docs
            
        except Exception as e:
            print(f"Error in get_symbol_prices: {e}")
            return []



if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(User)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass