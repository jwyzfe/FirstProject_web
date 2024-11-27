from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.routers import setup_routers
from app.database.database import init_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

from fastapi.staticfiles import StaticFiles
# url 경로, 자원 물리 경로, 프로그램밍 측면
import os
static_images_directory = os.path.join('app',"resources", "images")
app.mount("/images", StaticFiles(directory=static_images_directory), name="static_images")

# Router setup
setup_routers(app)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root(request: Request):
    # return RedirectResponse(url=f"/comodules/main")
    return RedirectResponse(url=f"/mains/home")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)