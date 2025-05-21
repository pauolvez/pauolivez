import asyncio
import sys
import os
from fastapi import FastAPI, Query
from app.auth import fastapi_users, auth_backend
from app.users import UserRead, UserCreate, UserUpdate
from app.models import User
from app.database import Base, engine
from app.ollama_client import generar_respuesta

from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info  # ✅ añadido
from dotenv import load_dotenv  # ✅ solo esta línea
from concurrent.futures import ThreadPoolExecutor

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
executor = ThreadPoolExecutor()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Rutas de autenticación
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/")
def root():
    return {"mensaje": "Backend FastAPI funcionando correctamente con fastapi-users 14"}

@app.get("/scrape")
async def scrape_url(url: str = Query(..., description="URL de la web a scrapear")):
    config = {
        "llm": {
            "api_key": openai_api_key,
            "model": "gpt-3.5-turbo",
            "temperature": 0,
        },
        "headless": True,
    }

    graph = SmartScraperGraph(
        prompt="Extrae la información más útil de esta web.",
        source=url,
        config=config
    )

    result = await asyncio.get_event_loop().run_in_executor(executor, graph.run)
    return {"datos": prettify_exec_info(result)}
