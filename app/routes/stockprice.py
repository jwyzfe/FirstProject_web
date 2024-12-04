from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database
from app.models.stockprice import Stockprice
collection_stockprice = Database(Stockprice)

from typing import Optional
@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
# http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
async def list(request:Request, page_number: Optional[int] = 1):
    user_dict = dict(request._query_params)
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    conditions = { }

    # try :
    #     conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
    # except:
    #     pass

    # stockprice_list, pagination = await collection_stockprice.getsbyconditionswithpagination(conditions
    #                                                                  ,page_number)
    # 심볼 요약 정보 조회 (페이지네이션)
    summaries, pagination = await collection_stockprice.get_symbol_summary_with_pagination(page_number=page_number)



    return templates.TemplateResponse(name="stockprice/list.html"
                                      , context={'request':request
                                                 , 'stockprices' : summaries
                                                  ,'pagination' : pagination })
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
# @router.get("/read/{object_id}")
# async def read(request:Request, object_id:PydanticObjectId):
#     stockprice = await collection_stockprice.get(object_id)
#     return templates.TemplateResponse(name="stockprice/read.html"
#                                       , context={'request':request
#                                                  , 'stockprice':stockprice})

@router.get("/read/{object_id}/{page_number}")
@router.get("/read/{object_id}")
async def read(request:Request, object_id:str, page_number: Optional[int] = 1):
        # 특정 심볼의 전체 주가 데이터 조회
    prices, pagination = await collection_stockprice.get_symbol_prices(object_id, page_number)
    return templates.TemplateResponse(name="stockprice/list_detail.html"
                                      , context={'request':request
                                                 , 'stockprices':prices
                                                 ,'pagination' : pagination
                                                 })