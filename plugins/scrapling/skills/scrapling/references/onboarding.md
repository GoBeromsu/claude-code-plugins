# Scrapling Setup

## Requirements

- Python 3.8+
- pip

## Installation

```bash
pip install "scrapling[fetchers]"
scrapling install
```

The `scrapling install` command downloads Playwright browsers (~100MB) needed for the StealthyFetcher and DynamicFetcher tiers.

## Verify

```bash
scrapling extract get 'https://httpbin.org/get' /tmp/test.md
cat /tmp/test.md
```
