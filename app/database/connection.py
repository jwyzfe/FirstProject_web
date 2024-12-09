from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from app.models.tossComments import tossComments
from app.models.dartAPI import dartAPI
from app.models.stockprice import Stockprice
from app.models.stocktwits import Stocktwits

from app.models.marketsenti import Marketsenti
from app.models.news_yahoo import News_yahoo
from datetime import datetime
from app.models.users import Hankyung #변경

import os
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[ Stockprice, Stocktwits, tossComments, dartAPI, Hankyung, Marketsenti,News_yahoo])




    class Config:
        env_file = os.path.join("app",".env")

from app.utils.paginations import Paginations

import json
class Database:
    def __init__(self, model):  #초기화 시 특정 모델과 연결
        self.model = model

    async def save(self, document):     #새 문서를 저장
        result = await document.create()
        return result

    async def get(self, id: PydanticObjectId):      #id로 문서를 검색
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self, conditions: dict = {}):     #주어진 조건(conditions)을 만족하는 모든 문서를 반환합니다.
        docs = await self.model.find_all(conditions).to_list()
        return docs

    # update with params json
    async def update_withjson(self, id: PydanticObjectId, body: json):      #json형식의 데이터로 문서를 업데이트
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

    async def delete(self, id: PydanticObjectId):       #특정 id를 가진 문서를 삭제합니다.
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    # column 값으로 Documents 가져오기
    async def getbyconditions(self, conditions:dict = {}) -> [Any]:     #조건을 만족하는 문서의 개수를 반환합니다.
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
    #MongoDB의 aggregate 명령을 사용해 조건에 맞는 문서를 반환
    async def aggregatebyconditions(self, conditions:list) -> [Any]:
        documents = await self.model.aggregate(conditions).to_list()  # find({})
        return documents    
#조건에 맞는 문서를 페이지네이션 방식으로 조회합니다.
    #페이지 수, 페이지당 문서 수, 정렬 방향(+ 또는 -) 등을 설정합니다.
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
                                             , records_per_page=10, pages_per_block=10
                                             , sorted = '-'
                                             , sort_field:str = 'create_date', ) -> [Any]:
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
            # 먼저 모든 유니크한 심볼 목록을 가져옴
            all_symbols = await self.model.distinct('SYMBOL')
            all_symbols.sort()  # 알파벳 순 정렬

            # 검색어가 있는 경우
            if 'SYMBOL' in conditions:
                filtered_symbols = [s for s in all_symbols if s == conditions['SYMBOL']]
            # 마켓 필터링
            elif 'market' in conditions:
                if conditions['market'] == 'kr':
                    filtered_symbols = [s for s in all_symbols if s.endswith(('.KS', '.KQ'))]
                elif conditions['market'] == 'us':
                    filtered_symbols = [s for s in all_symbols if not s.endswith(('.KS', '.KQ'))]
                else:
                    filtered_symbols = all_symbols
            else:
                filtered_symbols = all_symbols

            # 페이지네이션 계산
            total = len(filtered_symbols)
            pagination = Paginations(
                total_records=total,
                current_page=page_number,
                records_per_page=records_per_page,
                pages_per_block=pages_per_block
            )

            # 현재 페이지의 심볼만 선택
            start_idx = pagination.start_record_number
            end_idx = start_idx + pagination.records_per_page
            paged_symbols = filtered_symbols[start_idx:end_idx]
            
            # 선택된 심볼들의 최신 데이터 조회
            results = []
            for symbol in paged_symbols:
                doc = await self.model.find_one(
                    {"SYMBOL": symbol},
                    sort=[("CREATED_AT", -1)]
                )
                if doc:
                    results.append({
                        "SYMBOL": doc.SYMBOL,
                        "CREATED_AT": doc.CREATED_AT
                    })
            
            return results, pagination

        except Exception as e:
            print(f"Error in get_symbol_summary_with_pagination: {e}")
            return [], Paginations(
                total_records=0,
                current_page=page_number,
                records_per_page=records_per_page,
                pages_per_block=pages_per_block
            )




if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(User)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass