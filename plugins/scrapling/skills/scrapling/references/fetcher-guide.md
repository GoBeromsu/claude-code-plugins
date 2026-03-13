# Fetcher Selection Guide

## Decision Tree

```
URL to fetch?
├── defuddle already works? → use defuddle (faster, no Python)
├── defuddle returns empty/blocked?
│   ├── Static site, just needs stealth headers? → Fetcher
│   ├── Anti-bot / Cloudflare? → StealthyFetcher
│   └── JS-rendered SPA (React/Vue/Angular)? → DynamicFetcher
└── Need to interact (click, scroll, login)? → DynamicFetcher
```

## Fetcher Comparison

| Feature | Fetcher | StealthyFetcher | DynamicFetcher |
|---------|---------|-----------------|----------------|
| Speed | Fast | Slow (browser) | Slow (browser) |
| Playwright browser | No | Yes | Yes |
| Anti-bot bypass | Partial | Full | Full |
| Cloudflare Turnstile | No | Yes (solve_cloudflare) | Manual |
| JS rendering | No | Yes (headless) | Yes (full automation) |
| Click/scroll/interact | No | No | Yes |
| TLS fingerprint spoof | Yes | Yes | Yes |
| Memory usage | Low | High | High |

## When DynamicFetcher > StealthyFetcher

Use DynamicFetcher when you need to:
- **Click buttons** to load content (infinite scroll, "Load more")
- **Fill and submit forms** (login, search)
- **Wait for specific elements** to appear after user interaction
- **Execute JavaScript** on the page
- **Handle multi-step navigation** (login → dashboard → data)

StealthyFetcher is better when:
- Cloudflare Turnstile is the only obstacle
- Content loads automatically (no interaction needed)
- Speed matters — StealthyFetcher is optimized for anti-bot bypass specifically

## Installation by Fetcher Type

```bash
# All fetchers
pip install "scrapling[fetchers]"
scrapling install           # downloads Playwright browsers (~200MB)
scrapling install --force   # force reinstall browsers

# Parser only (no fetchers)
pip install scrapling
```

## Async Variants

Every fetcher has an async counterpart:

```python
import asyncio
from scrapling.fetchers import AsyncFetcher, AsyncStealthyFetcher, AsyncDynamicFetcher

async def main():
    page = await AsyncFetcher.fetch('https://example.com')
    print(page.get_all_text())

asyncio.run(main())
```

Session-based async (keep browser open across requests):

```python
from scrapling.fetchers import AsyncStealthySession

async with AsyncStealthySession(headless=True, max_pages=3) as session:
    pages = await asyncio.gather(
        session.fetch('https://example.com/page1'),
        session.fetch('https://example.com/page2'),
    )
```

## Version & Update Commands

```bash
# Check installed version
pip show scrapling

# Update to latest
pip install -U "scrapling[fetchers]"
scrapling install  # re-install browsers after update if needed

# Check if update is available
pip index versions scrapling 2>/dev/null | head -1
```
