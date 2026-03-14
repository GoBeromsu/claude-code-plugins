# Claude Code Plugins

A collection of custom Claude Code plugins for decision-making, developer workflows, web scraping, and Obsidian vault management.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| [common](plugins/common/) | antifragile, 5whys, first-principles, interview, scrapling | General-purpose thinking & scraping tools |
| [development](plugins/development/) | issue, docs, project-log | Developer workflow utilities |
| [obsidian](plugins/obsidian/) | obsidian-sync, terminology, youtube, obsidian-mermaid | Obsidian vault management |

## Install

```bash
# Add marketplace
claude plugins marketplace add GoBeromsu/claude-code-plugins

# Install plugins (user scope)
claude plugins install common@beomsu-koh --scope user
claude plugins install development@beomsu-koh --scope user
claude plugins install obsidian@beomsu-koh --scope user
```

## License

MIT
