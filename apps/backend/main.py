from fastapi import FastAPI

from .db.init_db import init_db
from .api import auth, products

app = FastAPI(title="King Star API")

app.include_router(auth.router)
app.include_router(products.router, prefix="/products", tags=["products"])


@app.on_event("startup")
def startup_event():
    init_db()
