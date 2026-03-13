---
name: project-log
description: "Log findings, decisions, and progress to a dedicated Agent note alongside the user's project log. Creates a paired Agent note to avoid edit conflicts with the user's own notes. Use when the user invokes /project-log, or says '노트에 적어줘', '기록해줘', '로그에 남겨', 'log this', '이거 적어두자', '진행상황 정리해줘', '이거 노트로 남겨', 'write this up', 'note this down'. NOT for editing user notes directly — user notes are read-only. NOT for daily notes — those are user-authored."
---

# Project Log

> **Note**: This skill works best with Obsidian vaults but can be adapted to any project that uses markdown files for documentation. Configure your project's note location in the project's `CLAUDE.md`.

The user writes their project log in markdown. You write to a separate **Agent note** that sits next to it. Two people working on the same project, each with their own notebook — no stepping on each other's work, no merge conflicts with the live editor.

```
<project-folder>/
  2026-03-04 <project>.md          <- user's note (never touch this)
  2026-03-04 <project>.agent.md    <- your note
```

The agent note links back to the user note via the `up:` frontmatter property. The `author: "[[claude code]]"` property identifies it as agent-authored.

## How it works

### 1. Figure out which project

Look at the current working directory's `CLAUDE.md` for project references, or infer from what you and the user have been discussing. If you're not sure, ask — a wrong guess means the note ends up in the wrong folder, which is worse than a quick question.

### 2. Find the project folder

Locate the project's note directory. Common patterns:

- Check `CLAUDE.md` for a configured notes path
- Look for existing `.agent.md` files in the project tree
- Use file search to find the project folder

```bash
# Example: find existing agent notes
find <project-root> -name "*.agent.md" -type f 2>/dev/null | head -5
```

### 3. Check what exists today

Read the user's note and any existing agent note for today:

```bash
# Check for today's notes
ls <project-folder>/<date>*
```

Date format is `YYYY-MM-DD`. The user note tells you what `up:` link to use. The agent note tells you what's already been logged today.

### 4. Write or update

**New note** — create with frontmatter + content. See `references/note-template.md` for the template and examples.

**Existing note** — read it first, then decide where new content belongs. The goal is to keep related things together, like a well-organized notebook — not a chronological dump. Follow this decision tree:

1. **Same topic, same heading** -> append bullets under the existing `##` section
2. **Same heading, later in the day** -> add a `### HH:MM` timestamp sub-heading, then append
3. **Different topic entirely** -> create a new `##` heading with a descriptive name

The key test: if you have to mentally context-switch to understand the new content relative to what's already under a heading, it belongs under a **new heading**. For example, "debugging a silent exit" and "understanding Node.js abstraction layers" are different topics even if they arose from the same session — give each its own `##`. Details and examples in `references/note-template.md`.

Use the `Read`, `Write`, and `Edit` tools for file operations.

## What goes in each section

Pick sections based on what you're actually logging. Skip anything that would be empty. These are common starting points, not a fixed set — create a descriptive `##` heading whenever content doesn't fit an existing section.

| Section | Use for |
|---|---|
| `## Findings` | What you discovered — codebase exploration, investigation results |
| `## Analysis` | Deep dives — PR reviews, architecture comparisons, trade-off analysis |
| `## Decisions` | What was decided and why — rationale matters more than the choice |
| `## Debug` | Debugging sessions — commands first, then narrative. See `references/note-template.md` for the full pattern |
| `## References` | Links, issues, PRs, docs that came up during the work |
| `## Progress` | What's done, what's left — checklist style |

Custom headings are encouraged when the content is a distinct topic. Good examples: `## Node.js Process Model`, `## API Rate Limiting Strategy`, `## Native Addon ABI Compatibility`. The heading should describe the topic, not the activity ("Process Model" not "What I Learned About Processes").

## Writing style

Match the language the user is using — Korean or English. Use `[[wikilinks]]` for internal notes (if using Obsidian) and `[text](url)` for external links.

Structure content as **nested bullet points** — a top-level bullet states the fact or decision, and sub-bullets provide supporting detail, rationale, or evidence. This mirrors how the user thinks: start with the headline, then drill into the why and how. Flat bullet lists lose the relationship between ideas.

For decisions specifically, the "why" is more valuable than the "what" — six months from now, the user won't remember *why* they chose approach A over B unless you recorded it. Every decision entry needs the rationale as a nested bullet, not just the conclusion.

Use code references like `` `path/to/file.ts:42` `` to make entries navigable.

For **debug entries**, commands and their outputs are the primary content — prose is secondary. A good debug log is one the user can copy-paste months later and reproduce the exact same investigation. Include the wrong turns too: misdiagnoses are the most valuable part of a debug log because they prevent future misdiagnoses. End every debug section with a concrete checklist of what to do differently next time.

One note per day per project. If you're logging multiple times in a session, everything goes to the same note — organized by topic, tracked by timestamps.

## Frontmatter conventions

When creating notes, use these frontmatter conventions (adapt as needed for your project):

- `status` values: `todo` / `inprogress` / `done` / `reviewed` / `stop` (lowercase, no hyphens)
- ISO 8601 dates, snake_case keys
- `author: "[[claude code]]"` on all agent-authored notes
- Wikilinks in frontmatter should be quoted: `up: "[[...]]"`
