from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from app.models.dartAPI import dartAPI
from typing import Optional
from beanie import PydanticObjectId

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")
collection_user = Database(dartAPI)

@router.get("/list/{page_number}")
@router.get("/list")
async def list(request: Request, page_number: Optional[int] = 1):
    user_dict = dict(request._query_params)
    conditions = {}

    # 검색 조건 처리
    if 'word' in user_dict and user_dict['word'].strip() and 'key_name' in user_dict:
        word = user_dict['word']
        key_name = user_dict['key_name']
        
        if key_name == 'CORP_CODE':
            conditions = {
                key_name: {"$regex": f"^{word}$", "$options": "i"}
            }
        elif key_name == 'BUSINESS_YEAR':
            conditions = {
                key_name: {"$regex": word, "$options": "i"}
            }

    # getsbyconditionswithpagination 메서드 사용
    comment_list, pagination = await collection_user.getsbyconditionswithpagination(
        conditions=conditions,
        page_number=page_number,
        records_per_page=10,  # 한 페이지당 보여줄 레코드 수
        pages_per_block=5     # 한 블록당 보여줄 페이지 수
    )

    return templates.TemplateResponse(
        name="dartAPI/list.html",
        context={
            'request': request,
            'comments': comment_list,
            'pagination': pagination
        }
    )