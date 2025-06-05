from .session import engine, SessionLocal
from ..models import user, product
from .base import Base
from ..models.user import User
from ..api.auth import get_password_hash


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "pauolivez").first():
            user = User(
                username="pauolivez",
                hashed_password=get_password_hash("paupaupau"),
                is_superuser=True,
            )
            db.add(user)
            db.commit()
    finally:
        db.close()
