import asyncio
import sys
from fastapi import FastAPI, Query
from app.auth import fastapi_users, auth_backend
from app.users import UserRead, UserCreate, UserUpdate
from app.models import User
from app.database import Base, engine
from app.ollama_client import query_ollama  # ✅ Cliente de Ollama
from app.scraper_graph import ejecutar_scraping_web  # ✅ ScrapeGraphAI con Ollama
from concurrent.futures import ThreadPoolExecutor

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
executor = ThreadPoolExecutor()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Rutas de autenticación
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"mensaje": "Backend FastAPI funcionando correctamente con fastapi-users 14 y Ollama"}

@app.get("/preguntar-ia")
async def preguntar_ia(pregunta: str = Query(..., min_length=3)):
    respuesta = await query_ollama(pregunta)
    return {"respuesta": respuesta}

@app.get("/scrap-web")
async def scrap_web(url: str = Query(..., min_length=10), instrucciones: str = Query(..., min_length=5)):
    resultado = await ejecutar_scraping_web(url, instrucciones)
    return {"resultado": resultado}