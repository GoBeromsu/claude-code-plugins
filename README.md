# Claude Code Plugins

A collection of custom Claude Code plugins for decision-making, developer workflows, web scraping, and Obsidian vault management.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| [thinking-tools](plugins/thinking-tools/) | antifragile, 5whys, first-principles, interview | Decision-making & analysis frameworks |
| [dev-tools](plugins/dev-tools/) | estimate, issue, docs, project-log | Developer workflow utilities |
| [scrapling](plugins/scrapling/) | scrapling | Anti-bot web scraping |
| [obsidian](plugins/obsidian/) | obsidian-sync, obsidian-doctor | Obsidian vault management |

## Install

```bash
# Install a specific plugin
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/thinking-tools

# Or install multiple
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/dev-tools
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/scrapling
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/obsidian
```

## License

MIT
