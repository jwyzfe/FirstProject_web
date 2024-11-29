from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database # app > database > connection 전부다 하위 개념
from app.models.financialstatements import FinancialStatements # app > models > financialstatements.py, import FinancialStatements 함수 
collection_user = Database(FinancialStatements)

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
'''
    원래 
    try :
        conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
    except:
        pass 여기까지 뜻하는게 뭘까? 여기서 무슨 에러가 생기는지 확인

    user_list, pagination = await collection_user.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="???/list.html"
                                      , context={'request':request
                                                 , '???' : ???_list
                                                  ,'pagination' : pagination })
'''

'''
   상훈님 stockprice_list, pagination = await collection_stockprice.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="stockprice/list.html"
                                      , context={'request':request
                                                 , 'stockprices' : stockprice_list
                                                  ,'pagination' : pagination })
'''
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}")
async def read(request:Request, object_id:PydanticObjectId):
    ??? = await collection_user.get(object_id)
    return templates.TemplateResponse(name="???/read.html"
                                      , context={'request':request
                                                 , '???':???})
