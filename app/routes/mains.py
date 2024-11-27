from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates/")

router = APIRouter()

@router.get("/home")
async def main(request: Request):
    context={'request':request}
    return templates.TemplateResponse(name="mains/home.html"
                                      , context=context)