from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from ..models.product import Product
from ..core import scraper

router = APIRouter()


@router.post("/search")
async def search_products(
    page_limit: int = Query(1, ge=1, le=5),
    crawl_depth: int = Query(0, ge=0, le=5),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    items = await scraper.search_and_compare(page_limit)
    if crawl_depth:
        crawled = await scraper.crawl_site(scraper.BOOKS_BASE, max_pages=crawl_depth)
        return {"products": items, "crawled": crawled}
    return items
