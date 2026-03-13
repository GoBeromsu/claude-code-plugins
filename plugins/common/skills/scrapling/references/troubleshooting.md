# Scrapling Troubleshooting

## Installation Issues

**`ModuleNotFoundError: No module named 'scrapling.fetchers'`**
```bash
# Wrong: pip install scrapling (parser only, no fetchers)
# Correct:
pip install "scrapling[fetchers]"
scrapling install
```

**`playwright._impl._errors.Error: Executable doesn't exist`**
```bash
scrapling install          # normal
scrapling install --force  # if normal didn't work
```

**Python version error**
- Scrapling requires Python 3.10+
- Check: `python --version`
- Fix: upgrade Python or use pyenv

## Fetching Issues

**StealthyFetcher returns empty page**
```python
# Try with solve_cloudflare=True
page = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True, network_idle=True)

# Or try DynamicFetcher as fallback
page = DynamicFetcher.fetch(url, headless=True, network_idle=True)
```

**Content missing (JS not loaded)**
```python
# Wrong: Fetcher doesn't run JS
page = Fetcher.fetch(url)

# Correct for JS-rendered pages:
page = DynamicFetcher.fetch(url, network_idle=True)
# network_idle=True waits until all XHR/fetch requests settle
```

**Site blocks headless browser detection**
```python
# Use StealthyFetcher — it spoofs fingerprints
page = StealthyFetcher.fetch(url, headless=True)

# Or impersonate a specific browser
page = Fetcher.fetch(url, impersonate='chrome124', stealthy_headers=True)
```

**Timeout errors**
```python
# Increase timeout (default is 30s)
page = StealthyFetcher.fetch(url, headless=True, timeout=60000)  # 60 seconds
```

## Selector Issues

**`get()` returns None**
```python
# provide a default value
title = page.css('h1::text').get('')  # returns '' instead of None
price = page.css('.price::text').get('N/A')
```

**Wrong content extracted**
```python
# Be specific with selectors
# Too broad:
page.css('p::text').getall()

# More specific:
page.css('article.content p::text').getall()
```

**Site redesigned, selector broke**
```python
# Use adaptive mode (requires auto_save=True on first run)
items = page.css('.product', auto_save=True)  # first run: saves fingerprint
items = page.css('.product', adaptive=True)   # later: re-finds by fingerprint
```

## MCP Server Issues

**`command not found: scrapling`**
```bash
pip install "scrapling[ai]"
which scrapling  # verify path
```

**MCP server not responding**
```bash
# Test manually
scrapling mcp  # should start without errors
```

## Version & Update

```bash
# Check version
pip show scrapling

# Update all extras
pip install -U "scrapling[all]"
scrapling install --force  # re-install browsers

# Rollback to specific version
pip install scrapling==0.2.9
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `import scrapling` fails | `pip install "scrapling[fetchers]"` |
| `page.css('.x').text` | Use `page.css('.x::text').get()` |
| Empty page with Fetcher | Use StealthyFetcher or DynamicFetcher |
| Slow scraping | Use Fetcher for static pages, async for bulk |
| Memory spike | Use `headless=True` and close sessions |
