from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)  # 👈 esto es obligatorio
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="vendedor", nullable=False)