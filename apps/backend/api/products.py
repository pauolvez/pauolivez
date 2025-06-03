eazwwx-codex/generar-estructura-base-backend-con-fastapi
from fastapi import APIRouter, Depends, Query

ueft9t-codex/generar-estructura-base-backend-con-fastapi
from fastapi import APIRouter, Depends, Query

from fastapi import APIRouter, Depends
main
main
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from ..models.product import Product
from ..core import scraper

router = APIRouter()


@router.post("/search")
eazwwx-codex/generar-estructura-base-backend-con-fastapi

ueft9t-codex/generar-estructura-base-backend-con-fastapi
main
async def search_products(
    page_limit: int = Query(1, ge=1, le=5),
    crawl_depth: int = Query(0, ge=0, le=5),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """Return example products and optional crawl info."""
    products = await scraper.search_and_compare(page_limit)
    result = {"products": products}
    if crawl_depth:
        result["crawled"] = await scraper.crawl_site(scraper.BOOKS_BASE, max_pages=crawl_depth)
    return result
eazwwx-codex/generar-estructura-base-backend-con-fastapi

  
async def search_products(db: Session = Depends(get_db), user=Depends(get_current_user)):
    products = await scraper.search_and_compare()
    # Here we just return the scraped products without saving
    return products
main
main
