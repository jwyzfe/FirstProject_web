from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
from beanie import PydanticObjectId
from app.database.connection import Database
from app.models.marketsenti import Marketsenti

##

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")
collection_marketsenti = Database(Marketsenti)


@router.get("/list/{page_number}")
@router.get("/list")
async def list(request: Request, page_number: Optional[int] = 1):

    user_dict = dict(request.query_params)
    query_params = dict(request.query_params)
    keyword = query_params.get("word","").strip()
    field = query_params.get("key_name", "")
    conditions = {}
    if keyword:  # 검색어가 입력된 경우
        try:
            if field in ["MACD_LINE", "RSI","MACD_HISTOGRAM", "SIGNAL_LINE"]:  # 숫자 필드 검색 처리
                conditions[field] = float(keyword)
            else:  # 문자열 필드 검색 처리
                conditions[field] = {"$regex": keyword, "$options": "i"}
        except ValueError:
            raise HTTPException(staues_code=400, detail="Invalid keyword format")

    marketsenti_list, pagination = await collection_marketsenti.getsbyconditionswithpagination(conditions 
        ,page_number,sort_field="TICKER"
    )
    
    pagination.query_params = f"key_name={field}&word={keyword}"
    
    return templates.TemplateResponse(
        "marketsenti/list.html",  # marketsenti_list와 pagination 데이터를 사용하여 HTML 페이지 생성
        {
            'request': request,
            'marketsenti_list': marketsenti_list,  # DB에서 가져온 데이터
            'pagination': pagination  # 페이지네이션 정보
        }
    )
    #breakpoint걸어놓고 request확인

# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}")
async def read(request: Request, object_id: PydanticObjectId):
    marketsenti = await collection_marketsenti.get(object_id)
    if not marketsenti:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return templates.TemplateResponse(
        "marketsenti/read.html",
        {
            'request': request,
            'marketsenti': marketsenti
        }
    )

