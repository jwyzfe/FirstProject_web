#FastAPI를 사용하여 웹 서버의 특정경로에 HTML템플릿을 렌더링 하는 핸들러 함수 

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from app.database.connection import Database
from app.models.news_yahoo import News_yahoo
from app.models.marketsenti import Marketsenti

templates = Jinja2Templates(directory="app/templates/")     #템플릿 파일이 위치한 경로를 지정합니다

router = APIRouter()

collection_news_yahoo = Database(News_yahoo)
collection_marketsenti = Database(Marketsenti)

@router.get("/home")        #브라우저에서 /home 경로로 접근하면 이 핸들러 함수가 실행됩니다.
async def main(request: Request):
    news_yahoo_list = await collection_news_yahoo.get_all()  # 모든 뉴스 데이터를 가져옵니다.
    marketsenti_list = await collection_marketsenti.get_all()  
    context={'request':request,
             'news_yahoo_list': news_yahoo_list,  
        'marketsenti_list': marketsenti_list}
    return templates.TemplateResponse(name="mains/senti.html"
                                      , context=context )
    
    
    
'''
클라이언트가 /home 경로로 GET 요청을 보냄.
main() 함수가 호출됨.
템플릿 mains/senti.html이 렌더링됨.
클라이언트는 HTML 페이지를 응답으로 받음.
'''
