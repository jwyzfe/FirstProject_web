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
    query_params = dict(request._query_params)
    conditions = {}

    # 검색 조건 구성
    if 'search_type' in query_params and 'search_word' in query_params and query_params['search_word']:
        search_word = query_params['search_word']
        
        if query_params['search_type'] == 'symbol':
            # Symbol은 정확히 일치
            conditions['SYMBOL'] = search_word
        elif query_params['search_type'] == 'content':
            # Content는 부분 일치
            conditions['CONTENT'] = {'$regex': search_word, '$options': 'i'}
        elif query_params['search_type'] == 'links':
            # Links는 부분 일치
            conditions['LINKS'] = {'$regex': search_word, '$options': 'i'}

    # 날짜 검색 조건 추가
    date_condition = {}
    if 'start_date' in query_params and query_params['start_date']:
        date_condition['$gte'] = query_params['start_date']
    if 'end_date' in query_params and query_params['end_date']:
        date_condition['$lte'] = query_params['end_date']
    
    if date_condition:
        conditions['TIME_DATA.DATE'] = date_condition

    # 심볼 요약 정보 조회 (페이지네이션)
    #summaries, pagination = await collection_stockprice.get_symbol_summary_with_pagination(page_number=page_number)

    summaries, pagination = await collection_stockprice.getsbyconditionswithpagination(
        conditions, page_number)


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
    query_params = dict(request._query_params)
    conditions = {'SYMBOL': object_id}  # 기본 조건으로 symbol 설정

    # 날짜 검색 조건 추가
    date_condition = {}
    if 'start_date' in query_params and query_params['start_date']:
        date_condition['$gte'] = query_params['start_date']
    if 'end_date' in query_params and query_params['end_date']:
        date_condition['$lte'] = query_params['end_date']
    
    if date_condition:
        # 임베디드 구조의 TIME_DATA.DATE 필드에 대한 조건 설정
        conditions['TIME_DATA.DATE'] = date_condition
            
    prices, pagination = await collection_stockprice.get_symbol_prices(
        symbol=object_id, 
        page_number=page_number,
        start_date=query_params.get('start_date'),
        end_date=query_params.get('end_date')
    )
    
    return templates.TemplateResponse(
        name="stockprice/list_detail.html",
        context={
            'request': request,
            'stockprices': prices,
            'pagination': pagination
        })