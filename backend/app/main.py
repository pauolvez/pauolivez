from fastapi import FastAPI
from app.auth import auth_router, register_router
from app.database import Base, engine

app = FastAPI()

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

# Rutas de autenticación
app.include_router(auth_router, prefix="/auth/jwt", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])

@app.get("/")
def home():
    return {"mensaje": "Backend conectado a base de datos correctamente"}