# Claude Code Plugins

A collection of custom Claude Code plugins for decision-making, developer workflows, web scraping, and Obsidian vault management.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| [common](plugins/common/) | antifragile, 5whys, first-principles, interview, scrapling | General-purpose tools |
| [development](plugins/development/) | issue, docs, project-log | Developer workflow utilities |
| [obsidian](plugins/obsidian/) | obsidian-sync, terminology, youtube | Obsidian vault management |

## Install

```bash
# Install a specific plugin
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/common

# Or install multiple
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/development
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/obsidian
```

## License

MIT
