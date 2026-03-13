---
name: scrapling
description: |
  Fetch web content using Scrapling — bypasses anti-bot protection, Cloudflare, and JS-rendered pages. Use this skill instead of defuddle when: (1) defuddle returns empty, blocked, or incomplete content, (2) the URL is behind Cloudflare or other anti-bot systems, (3) the page requires JavaScript rendering, (4) the user mentions "anti-bot", "Cloudflare", "JS rendering", "scraping", or provides a URL from known blocker sites (LinkedIn, Instagram, Amazon, Twitter/X, etc.). Also use when user explicitly says "scrapling으로 가져와줘" or "scrapling 써서". Do NOT use for simple static pages where defuddle already works.
---

## How to fetch content with this skill

Your job is to **fetch the URL and return the content** — not to explain Scrapling to the user.

### Step 1: Pick the right fetcher tier

| Signal | Command |
|--------|---------|
| General blocked / unknown | `scrapling extract get` (Fetcher — fast, no browser) |
| Anti-bot / Cloudflare | `scrapling extract stealthy-fetch --solve-cloudflare` |
| JS-rendered / SPA / React | `scrapling extract fetch` (DynamicFetcher — full browser) |

When in doubt, start with `get`. If the result is thin (< 200 chars), escalate automatically.

### Step 2: Run the command

```bash
# Tier 1: Fast HTTP (no browser)
scrapling extract get 'URL' /tmp/scrapling_out.md

# Tier 2: Stealth browser (anti-bot bypass)
scrapling extract stealthy-fetch 'URL' /tmp/scrapling_out.md

# Tier 3: Full browser (JS-rendered pages)
scrapling extract fetch 'URL' /tmp/scrapling_out.md

# Narrow to a section with CSS selector
scrapling extract get 'URL' /tmp/scrapling_out.md --css-selector 'main, article, #content'
```

Then read `/tmp/scrapling_out.md` and return the content to the user.

### Step 3: Escalation logic

```
Try Tier 1 (get)
  → if content < 200 chars or clearly blocked → Try Tier 2 (stealthy-fetch)
  → if still failing → Try Tier 3 (fetch)
```

Tell the user which tier was used (e.g., "Fetched using StealthyFetcher due to anti-bot protection").

---

## If scrapling CLI isn't installed

```bash
pip install "scrapling[fetchers]"
scrapling install    # downloads Playwright browsers (~100MB)
```

---

## Fetching structured data (not just reading content)

If the user wants specific data extracted (prices, links, table rows, etc.) rather than full page content, use a short Python script:

```python
from scrapling.fetchers import Fetcher  # or StealthyFetcher, DynamicFetcher

page = Fetcher.fetch('URL', stealthy_headers=True)

# CSS selectors (Scrapy style)
results = page.css('.selector::text').getall()
# or
item = page.css('.selector::text').get()

print(results)
```

See `references/selectors.md` for full selector syntax.
See `references/fetcher-guide.md` for when to use which fetcher.
See `references/troubleshooting.md` if you hit installation or fetch errors.
