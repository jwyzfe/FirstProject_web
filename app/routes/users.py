from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database
from app.models.users import User
collection_user = Database(User)

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

    try :
        conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
    except:
        pass

    user_list, pagination = await collection_user.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="users/list.html"
                                      , context={'request':request
                                                 , 'users' : user_list
                                                  ,'pagination' : pagination })
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}")
async def read(request:Request, object_id:PydanticObjectId):
    user = await collection_user.get(object_id)
    return templates.TemplateResponse(name="users/read.html"
                                      , context={'request':request
                                                 , 'user':user})

