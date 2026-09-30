from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db

init_db()
from .routers import auth_routes, page_routes, recommendation_routes

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app=FastAPI(title=settings.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(page_routes.router)
app.include_router(auth_routes.router)
app.include_router(recommendation_routes.router)

@app.get("/health")
def health(): return {"status":"ok"}
