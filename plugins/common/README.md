# common

General-purpose tools for Claude Code — decision-making frameworks and web scraping.

## Skills

| Skill | Description |
|-------|-------------|
| `/common:antifragile` | Apply Taleb's Barbell Strategy to decisions |
| `/common:5whys` | Interactive root-cause analysis (5+ rounds) |
| `/common:first-principles` | Decompose problems to irreducible fundamentals |
| `/common:interview` | Probe plans for blind spots before implementation |
| `/common:scrapling` | Fetch web content bypassing anti-bot protection |

## Prerequisites

- **scrapling**: `pip install "scrapling[fetchers]" && scrapling install`

## Install

```bash
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/common
```

## License

MIT
