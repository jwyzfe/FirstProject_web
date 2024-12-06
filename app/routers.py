from app.routes.mains import router as mains_router
from app.routes.users import router as user_router

# def setup_routers(app):
#     app.include_router(mains_router, prefix="/mains")
#     app.include_router(user_router, prefix="/users")

'''위를 참고하여 변경'''

def setup_routers(app):
    # app.include_router(mains_router, prefix="/DB_SGMN")
    app.include_router(mains_router, prefix="/mains")
    app.include_router(user_router, prefix="/articles")