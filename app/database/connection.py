from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from app.models.users import Hankyung #변경

import os
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[Hankyung]) #변경

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
                                             , sort_field:str = 'create_date') -> [Any]:
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


if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(User)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass