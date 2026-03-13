# scrapling

Anti-bot web scraping skill for Claude Code using [Scrapling](https://github.com/D4Vinci/Scrapling).

## Skill

| Skill | Description |
|-------|-------------|
| `/scrapling:scrapling` | Fetch web content bypassing anti-bot protection |

Automatically escalates through three tiers:
1. **Fast HTTP** — standard fetch (Fetcher)
2. **Stealth browser** — anti-bot bypass (StealthyFetcher)
3. **Full browser** — JS-rendered pages (DynamicFetcher)

## Prerequisites

```bash
pip install "scrapling[fetchers]"
scrapling install    # downloads Playwright browsers (~100MB)
```

## Install

```bash
claude plugin add github:beomsu/claude-code-plugins --path plugins/scrapling
```

## License

MIT
