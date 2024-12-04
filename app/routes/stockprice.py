from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")
from datetime import datetime
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
            conditions['SYMBOL'] = search_word.upper()
        elif query_params['search_type'] == 'content':
            # Content는 부분 일치
            conditions['CONTENT'] = {'$regex': search_word, '$options': 'i'}
        elif query_params['search_type'] == 'links':
            # Links는 부분 일치
            conditions['LINKS'] = {'$regex': search_word, '$options': 'i'}

    # 심볼 요약 정보 조회 (페이지네이션)
    summaries, pagination = await collection_stockprice.get_symbol_summary_with_pagination(
        conditions=conditions,
        page_number=page_number)

    # summaries, pagination = await collection_stockprice.getsbyconditionswithpagination(
    #     conditions, page_number)


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
        start_datetime = datetime.strptime(query_params['start_date'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        date_condition['$gte'] = start_datetime
    if 'end_date' in query_params and query_params['end_date']:
        end_datetime = datetime.strptime(query_params['end_date'], '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        date_condition['$lte'] = end_datetime
    if date_condition:
        conditions['TIME_DATA.DATE'] = date_condition

    # 가격 검색 조건 추가
    if all(key in query_params for key in ['price_field', 'comparison', 'price_value']) and query_params['price_value']:
        price_field = query_params['price_field']
        comparison = query_params['comparison']
        try:
            price_value = float(query_params['price_value'])
            
            # MongoDB 쿼리 연산자 매핑
            operator = '$gte' if comparison == 'gte' else '$lte'
            
            # 임베디드 구조에 맞게 필드 이름 구성
            field_name = f'TIME_DATA.PRICE_DATA.{price_field}'
            conditions[field_name] = {operator: price_value}
        except ValueError:
            pass  # 숫자 변환 실패 시 무시

    print("Search conditions:", conditions)  # 디버깅용 출력
            
    prices, pagination = await collection_stockprice.getsbyconditionswithpagination(
        conditions=conditions,
        page_number=page_number,
        sort_field='TIME_DATA.DATE'
    )
    
    # 결과 변환 (임베디드 구조를 평탄화)
    transformed_prices = []
    for doc in prices:
        transformed_doc = {
            "_id": doc.id,
            "SYMBOL": doc.SYMBOL,
            "DATE": doc.TIME_DATA.DATE,
            "OPEN": doc.TIME_DATA.PRICE_DATA.OPEN,
            "HIGH": doc.TIME_DATA.PRICE_DATA.HIGH,
            "LOW": doc.TIME_DATA.PRICE_DATA.LOW,
            "CLOSE": doc.TIME_DATA.PRICE_DATA.CLOSE,
            "VOLUME": doc.TIME_DATA.PRICE_DATA.VOLUME,
            "STOCKSPLITS": doc.TIME_DATA.PRICE_DATA.STOCKSPLITS,
            "DIVIDENDS": doc.TIME_DATA.PRICE_DATA.DIVIDENDS,
            "CREATED_AT": doc.CREATED_AT
        }
        transformed_prices.append(transformed_doc)
    
    return templates.TemplateResponse(
        name="stockprice/list_detail.html",
        context={
            'request': request,
            'stockprices': transformed_prices,
            'pagination': pagination
        })