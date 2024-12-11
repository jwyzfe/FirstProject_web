from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from app.models.youtubeComments import youtubeComments
from typing import Optional
from beanie import PydanticObjectId

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")
collection_user = Database(youtubeComments)

@router.get("/list/{page_number}")
@router.get("/list")
async def list(request: Request, page_number: Optional[int] = 1):
    user_dict = dict(request._query_params)
    conditions = {}

    # 검색 조건 처리
    if 'word' in user_dict and user_dict['word'].strip() and 'key_name' in user_dict:
        word = user_dict['word']
        key_name = user_dict['key_name']
        
        if key_name == 'SYMBOL':
            # Symbol 검색: 대소문자 구분 없이 정확한 매칭
            conditions = {
                key_name: {"$regex": f"^{word}$", "$options": "i"}
            }
        elif key_name == 'COMMENT':
            # Comment 검색: 대소문자 구분 없이 부분 매칭
            conditions = {
                key_name: {"$regex": word, "$options": "i"}
            }

    # 페이지네이션과 함께 데이터 조회
    comment_list, pagination = await collection_user.getsbyconditionswithpagination(
        conditions, page_number
    )

    return templates.TemplateResponse(
        name="tossComments/list.html",
        context={
            'request': request,
            'comments': comment_list,
            'pagination': pagination
        }
    )

@router.get("/read/{object_id}")
async def read(request: Request, object_id: PydanticObjectId):
    comment = await collection_user.get(object_id)
    return templates.TemplateResponse(
        name="tossComments/read.html",
        context={
            'request': request,
            'comment': comment
        }
    )