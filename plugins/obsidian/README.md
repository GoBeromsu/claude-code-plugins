# obsidian

Obsidian vault management utilities for Claude Code.

## Skills

| Skill | Description |
|-------|-------------|
| `/obsidian:obsidian-sync` | Manage headless Obsidian Sync between machines |
| `/obsidian:obsidian-doctor` | Diagnose and fix stale paths after vault restructuring |

## Prerequisites

- **obsidian-sync**: `npm install -g obsidian-headless` (Node.js 22+)
- **obsidian-doctor**: Obsidian vault with `.obsidian/` config directory

## Install

```bash
claude plugin add github:beomsu/claude-code-plugins --path plugins/obsidian
```

## License

MIT
