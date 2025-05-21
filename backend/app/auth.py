from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models import User
from app.database import SessionLocal
from fastapi_users import models
from app.config import settings

# Modelos de usuario
class UserRead(models.BaseUser[int]):
    role: str

class UserCreate(models.BaseUserCreate):
    role: str

class UserUpdate(models.BaseUserUpdate):
    role: str


# JWT
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600 * 24 * 7)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Conexión base de datos
async def get_user_db():
    db = SessionLocal()
    yield SQLAlchemyUserDatabase(User, db)

fastapi_users = FastAPIUsers[User, int](
    get_user_db,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
