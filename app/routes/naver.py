# from app.database.connection import Database
# from fastapi import APIRouter, Depends, HTTPException, status

# router = APIRouter()

# from fastapi.templating import Jinja2Templates
# from fastapi import Request

# templates = Jinja2Templates(directory="app/templates/")

# from app.database.connection import Database
# from app.models.users import User
# collection_user = Database(User)

# from typing import Optional
# @router.get("/list/{page_number}")
# @router.get("/list") # 검색 with pagination
# # http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# # http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# # http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
# async def list(request:Request, page_number: Optional[int] = 1):
#     user_dict = dict(request._query_params)
#     # db.answers.find({'name':{ '$regex': '김' }})
#     # { 'name': { '$regex': user_dict.word } }
#     conditions = { }

#     try :
#         conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
#     except:
#         pass

#     user_list, pagination = await collection_user.getsbyconditionswithpagination(conditions
#                                                                      ,page_number)
#     return templates.TemplateResponse(name="users/list.html"
#                                       , context={'request':request
#                                                  , 'users' : user_list
#                                                   ,'pagination' : pagination })
# from beanie import PydanticObjectId
# # 회원 상세정보 /users/read -> users/read.html
# # Path parameters : /users/read/id or /users/read/uniqe_name
# @router.get("/read/{object_id}")
# async def read(request:Request, object_id:PydanticObjectId):
#     user = await collection_user.get(object_id)
#     return templates.TemplateResponse(name="users/read.html"
#                                       , context={'request':request
#                                                  , 'user':user})

'''위 내용 참고하여 변경'''
from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database
from app.models.naver_reply import Naver_reply
collection_naver = Database(Naver_reply)

from typing import Optional

# 1. 댓글 목록 조회 with Pagination

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination 
# http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
async def list_naver(request:Request, page_number: Optional[int] = 1):
    query_params = dict(request.query_params)
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    conditions = { }

    # 검색 조건 설정(예: 제목 검색)
    try :
        # conditions = {query_params['key_name'] : { '$regex': query_params["word"] }} 변경전
        key_name = query_params.get('key_name',None)
        word = query_params.get('word',None)
        if key_name and word:
            conditions = {key_name: {'$regex' : word}}
    except Exception as e:
        print(f"Error processing query params: {e}")
    
    print("Conditions:", conditions)

    reply_list, pagination = await collection_naver.getsbyconditionswithpagination(conditions
                                                                     ,page_number,sort_field="날짜")
    return templates.TemplateResponse(name="naver/list.html"
                                      , context={'request':request
                                                 , 'reply' : reply_list
                                                  ,'pagination' : pagination })
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name

# 2. 댓글 상세 조회
# /articles/read/{{article.id}}
@router.get("/read/{object_id}")
async def read_naver(request:Request, object_id:PydanticObjectId):
    naver_reply = await collection_naver.get(object_id)
    if naver_reply is None:
        raise HTTPException(status_code=404, detail="naver_reply not found")
    
    return templates.TemplateResponse(name="naver_router/read.html"
                                      , context={'request':request
                                                 , 'reply':naver_reply})
    