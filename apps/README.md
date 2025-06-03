# King Star Project

This folder contains a demo backend built with FastAPI and a minimal React frontend.
It includes an example scraper that uses [Books to Scrape](https://books.toscrape.com) as an allowed data source.

## Setup

```bash
python -m pip install -r requirements.txt
# Install browser binaries for Playwright
python -m playwright install
```

Launch backend and frontend on Windows using `start.bat`.

## Notes
- The scraper uses Playwright to render pages with JavaScript support and automatically scans the rendered DOM for price values.
- Only scrape websites that explicitly allow it and comply with their terms of service.
