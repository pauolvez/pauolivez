# Scraper Usage Guide

This document explains how to try the sample scraper included in the **King Star** project.

## 1. Install dependencies

```bash
python -m pip install -r apps/requirements.txt
python -m playwright install
```

## 2. Start the application

On Windows you can run:

```cmd
apps\start.bat
```

This launches the FastAPI backend and the React frontend.

## 3. Authenticate

The database already includes an initial user so you can log in immediately:

```
username: pauolivez
password: paupaupau
```

Send a POST request to `/login` with these credentials to obtain a token.

## 4. Choose a website to scrape

The scraper is configured by default to read the public demo site **Books to Scrape**. To target another website that explicitly allows scraping, edit the constant `BOOKS_BASE` in `apps/backend/core/scraper.py` and set it to the base URL of the permitted site.

```
BOOKS_BASE = "https://example.com/"
```

Only scrape websites that provide permission in their terms of service or robots.txt.

## 5. Run the scraper

Call the `/products/search` endpoint with your authentication token. You can control how many pages are scanned with the `page_limit` parameter and enable the simple crawler with `crawl_depth`.

Example with `curl`:

```bash
curl -X POST "http://localhost:8000/products/search?page_limit=2&crawl_depth=3" -H "Authorization: Bearer <TOKEN>"
```

The endpoint returns a list of products and, if `crawl_depth` is greater than zero, the pages found by the crawler.

Use these results responsibly and respect each website's usage policy.
