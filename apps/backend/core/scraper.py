"""Dynamic scraping utilities for sites that allow it."""

from urllib.parse import urljoin

import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

BOOKS_BASE = "https://books.toscrape.com/"

# Regex to detect typical price patterns (e.g. $10.99, 8,50 €, £5.00)
PRICE_RE = re.compile(r"([\$€£]\s*\d+[\d,.]*)")


async def _load_html(page, url: str) -> str:
    """Navigate with Playwright and return rendered HTML."""
    await page.goto(url)
    return await page.content()


def extract_price_tags(html: str):
    """Return list of elements that look like prices."""
    soup = BeautifulSoup(html, "html.parser")
    tags = []
    for el in soup.find_all(True):
        text = el.get_text(strip=True)
        if text and PRICE_RE.search(text):
            tags.append({"tag": el.name, "text": text})
    return tags


async def fetch_books(page_limit: int = 1):
    """Scrape example products from books.toscrape.com using Playwright."""
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for idx in range(1, page_limit + 1):
            url = f"{BOOKS_BASE}catalogue/page-{idx}.html"
            html = await _load_html(page, url)
            soup = BeautifulSoup(html, "html.parser")
            for art in soup.select("article.product_pod"):
                title = art.h3.a.get("title", "")
                price_text = art.select_one(".price_color").text
                price = float(price_text.lstrip("£"))
                img = urljoin(BOOKS_BASE, art.find("img")["src"])
                items.append({"name": title, "image": img, "supplier_price": price})
        await browser.close()
    return items


async def crawl_site(start_url: str, max_pages: int = 5):
    """Naive crawler that follows links within the same domain."""
    visited = set()
    to_visit = [start_url]
    found = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
            visited.add(url)
            html = await _load_html(page, url)
            soup = BeautifulSoup(html, "html.parser")
            found.append({"url": url, "title": soup.title.string if soup.title else ""})
            for link in soup.find_all("a", href=True):
                new_url = urljoin(start_url, link["href"])
                if new_url.startswith(start_url) and new_url not in visited:
                    to_visit.append(new_url)
        await browser.close()
    return found


async def detect_prices(url: str):
    """Load a page and return any elements that contain prices."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        html = await _load_html(page, url)
        await browser.close()
    return extract_price_tags(html)


async def search_and_compare(page_limit: int = 1):
    """Return scraped products with placeholder Amazon data."""
    products = await fetch_books(page_limit)
    for item in products:
        item["amazon_price"] = round(item["supplier_price"] * 1.5, 2)
        item["asin"] = ""
        item["profit_fba"] = item["amazon_price"] - item["supplier_price"]
        item["profit_ds"] = item["profit_fba"] - 1.0
        item["estimated_sales"] = 10
    return products
