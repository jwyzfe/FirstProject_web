from app.routes.mains import router as mains_router
from app.routes.users import router as user_router
from app.routes.stockprice import router as stockprice_router
from app.routes.stocktwits import router as stocktwits_router

def setup_routers(app):
    app.include_router(mains_router, prefix="/mains")
    app.include_router(user_router, prefix="/users")
    app.include_router(stockprice_router, prefix="/stockprice")
    app.include_router(stocktwits_router, prefix="/stocktwits")
