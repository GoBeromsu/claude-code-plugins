# obsidian

Obsidian vault management utilities for Claude Code.

## Skills

| Skill | Description |
|-------|-------------|
| `/obsidian:obsidian-sync` | Manage headless Obsidian Sync between machines |
| `/obsidian:terminology` | Create, rewrite, and consolidate PKM terminology notes with variant detection and duplicate merging |
| `/obsidian:youtube` | Extract YouTube transcripts and convert into Korean article clippings |

## Prerequisites

- `npm install -g obsidian-headless` (Node.js 22+)
- `yt-dlp` (for youtube skill): `brew install yt-dlp`

## Install

```bash
claude plugin add github:GoBeromsu/claude-code-plugins --path plugins/obsidian
```

## License

MIT
