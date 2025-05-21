import asyncio
import sys
from fastapi import FastAPI, Query
from app.auth import fastapi_users, auth_backend
from app.users import UserRead, UserCreate, UserUpdate
from app.models import User
from app.database import Base, engine
from app.scraper import buscar_productos_aliexpress


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()


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

@app.get("/buscar-productos")
async def buscar_productos(query: str = Query(..., min_length=2)):
    resultados = await buscar_productos_aliexpress(query)
    return {"resultados": resultados}
