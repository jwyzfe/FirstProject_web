from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database
from app.models.news_yahoo import News_yahoo
collection_news_yahoo = Database(News_yahoo)

from typing import Optional
@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
# http://127.0.0.1:8000/users/list_jinja _pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
async def list(request:Request, page_number: Optional[int] = 1):
    user_dict = dict(request.query_params)
   
    conditions = {}
    
    news_yahoo_list, pagination = await collection_news_yahoo.getsbyconditionswithpagination(conditions 
                                                                     ,page_number)
    return templates.TemplateResponse(name="news_yahoo/list.html"
                                      , context={'request':request
                                                 , 'news_yahoo_list' : news_yahoo_list   # db데이터 연결 이게 templates로 연결
                                                  ,'pagination' : pagination })
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}")
async def read(request:Request, object_id:PydanticObjectId):
    news_yahoo = await collection_news_yahoo.get(object_id)
    return templates.TemplateResponse(name="news_yahoo/read.html"
                                      , context={'request':request
                                                 , 'news_yahoo':news_yahoo})

