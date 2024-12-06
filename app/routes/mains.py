from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates/")

router = APIRouter()

@router.get("/home")
async def main(request: Request):
    context={'request':request}
    return templates.TemplateResponse(name="mains/home.html"
                                      , context=context)
    
    # 라우터를 타고 메인함수를 들어와서 home과 mains 결합(?)해서 화면에표출
''' 위내용 참고하여 변경 
chat gpt 답변 : from app.routes.mains import router as mains_router에서 mains라는 이름이 중복되면 충돌 가능성이 있습니다. '''
# from fastapi import APIRouter, Depends, HTTPException, status, Request
# from fastapi.templating import Jinja2Templates

# templates = Jinja2Templates(directory="app/templates/")

# router = APIRouter()

# @router.get("/COL_SCRAPPING_HANKYUNG_HISTORY")
# async def main(request: Request):
#     context={'request':request}
#     return templates.TemplateResponse(name="/DB_SGMN/COL_SCRAPPING_HANKYUNG_HISTORY.html"
#                                       , context=context)
    
    # name = "/DB_SGMN/ 과 어떤게 결합되어야 정상적으로 나올지?"
