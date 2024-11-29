from app.routes.mains import router as mains_router
from app.routes.users import router as user_router
from app.routes.??? import router as ???
from app.routes.??? import router as ???


def setup_routers(app):
    app.include_router(mains_router, prefix="/mains")
    app.include_router(user_router, prefix="/users")
    app.???_router(???_router, prefix="/???")
    app.???_router(???_router, prefix="/???")
    # 