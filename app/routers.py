from app.routes.mains import router as mains_router
from app.routes.users import router as user_router
from app.routes.marketsenti import router as marketsenti_router
from app.routes.news_yahoo import router as news_yahoo_router
def setup_routers(app):
    app.include_router(mains_router, prefix="/mains")
    app.include_router(user_router, prefix="/users")#marketsenti
    app.include_router(marketsenti_router, prefix="/marketsenti")#marketsenti
    app.include_router(news_yahoo_router, prefix="/news_yahoo")