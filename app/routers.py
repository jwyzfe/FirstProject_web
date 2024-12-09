from app.routes.mains import router as mains_router
from app.routes.tossComments import router as tossComments_router
from app.routes.dartAPI import router as dartAPI_router
from app.routes.stockprice import router as stockprice_router
from app.routes.stocktwits import router as stocktwits_router
from app.routes.hankyung_article import router as user_router

from app.routes.marketsenti import router as marketsenti_router
from app.routes.news_yahoo import router as news_yahoo_router
# def setup_routers(app):
#     app.include_router(mains_router, prefix="/mains")
#     app.include_router(user_router, prefix="/users")

'''위를 참고하여 변경'''

def setup_routers(app):
    # app.include_router(mains_router, prefix="/DB_SGMN")
    app.include_router(mains_router, prefix="/mains")
    app.include_router(user_router, prefix="/articles")
    app.include_router(tossComments_router, prefix="/tossComments")
    app.include_router(dartAPI_router, prefix="/dartAPI")
    app.include_router(stockprice_router, prefix="/stockprice")
    app.include_router(stocktwits_router, prefix="/stocktwits")
    app.include_router(marketsenti_router, prefix="/marketsenti")#marketsenti
    app.include_router(news_yahoo_router, prefix="/news_yahoo")
