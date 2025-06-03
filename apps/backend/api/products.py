from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from ..models.product import Product
from ..core import scraper

router = APIRouter()


@router.post("/search")
async def search_products(db: Session = Depends(get_db), user=Depends(get_current_user)):
    products = await scraper.search_and_compare()
    # Here we just return the scraped products without saving
    return products
