from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from app.database.connection import Database
from app.models.news_yahoo import News_yahoo
from beanie import PydanticObjectId


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")
collection_news_yahoo = Database(News_yahoo)

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination

async def list(request:Request, page_number: Optional[int] = 1):
    user_dict = dict(request.query_params)
    query_params = dict(request.query_params)
    keyword = query_params.get("word","").strip()
    field = query_params.get("key_name", "")
    conditions = {}
    if keyword:  # 검색어가 입력된 경우
        try:
            if field in ["TITLE", "CONTENTS"]:  # 문자열 필드 검색 처리
                conditions[field] = {"$regex": keyword, "$options": "i"}  # 대소문자 구분 없이 검색
            elif field == "DATE":  # DATE는 문자열이 아닌 경우도 대비
                conditions[field] = keyword  # DATE 검색 조건 예외 처리 필요 시 여기에 작성
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid keyword format: {e}")

    
    news_yahoo_list, pagination = await collection_news_yahoo.getsbyconditionswithpagination(conditions 
        ,page_number
    )
    pagination.query_params = f"key_name={field}&word={keyword}"
    
    return templates.TemplateResponse(
        "news_yahoo/list.html",  # marketsenti_list와 pagination 데이터를 사용하여 HTML 페이지 생성
        {
            'request': request,
            'news_yahoo_list': news_yahoo_list,  # DB에서 가져온 데이터
            'pagination': pagination  # 페이지네이션 정보
        }
    )

# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name

@router.get("/read/{object_id}")
async def read(request: Request, object_id: PydanticObjectId):
    news_yahoo = await collection_news_yahoo.get(object_id)
    if not news_yahoo:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return templates.TemplateResponse(
        "news_yahoo/read.html",
        {
            'request': request,
            'news_yahoo': news_yahoo
        }
    )

