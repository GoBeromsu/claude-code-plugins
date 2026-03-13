# Agent Note Template

## Frontmatter

Every agent note starts with this frontmatter. The `up:` link creates a backlink to the user's daily log so they stay paired.

```yaml
---
aliases: []
date_created: <YYYY-MM-DD>
date_modified: <YYYY-MM-DD>
tags: []
type: log
author: "[[claude code]]"
up:
  - "[[<date> <project>]]"
---
```

## Full example

```markdown
---
aliases: []
date_created: 2026-03-04
date_modified: 2026-03-04
tags: []
type: log
author: "[[claude code]]"
up:
  - "[[2026-03-04 2026 Google Summer of Code]]"
---

## Findings
- `packages/core/src/tools/tools.ts` — tool registry uses decorator pattern
	- 60+ tools registered via `@Tool()` decorator with metadata
	- Each tool defines `name`, `description`, `parameters` (Zod schema)
- MCP integration in `packages/core/src/mcp/`
	- External tool providers connect via Model Context Protocol
	- Config lives in `.gemini/settings.json` under `mcpServers`

## Decisions
- **OAuth silent exit analysis**: chose issue #14943
	- Why: P1 + help-wanted label, clear repro steps, existing PR #17439 as reference
	- Alternative: #20213 also related but broader scope, less suitable as first contribution
	- Trade-off: security-related code may face stricter review

## References
- [#14943 — OAuth silent failure](https://github.com/google-gemini/gemini-cli/issues/14943)
- [[2026-03-04 2026 Google Summer of Code]] — user log
```

## Organizing existing notes

When the note already has content, read it first and think about where new information belongs. The principle: **group by context, not by time**. A well-organized note reads like a reference document, not a chat log.

Use this decision tree:

### Case 1: Same topic, same heading -> append

The new content is about the same subject as an existing `##` section. Append bullets directly, optionally with a `### HH:MM` timestamp to mark when it was added.

```markdown
## Findings
- `packages/core/src/tools/tools.ts` — tool registry uses decorator pattern
- `packages/core/src/tools/tools.ts:128` — tools registered via `@Tool()` decorator with metadata

### 15:30
- `packages/core/src/tools/tools.ts:200` — tool parameters validated via Zod at registration time
```

### Case 2: Different topic -> new `##` heading

The new content requires a mental context-switch from what's already in the note. Create a new `##` heading with a descriptive name that captures the topic, not the activity.

Good: `## Node.js Process Model`, `## Native Addon ABI Compatibility`
Bad: `## New Findings`, `## Additional Content`

```markdown
## Debug
- **Symptom**: `npm start` silent exit
- **Root cause**: Native addon built with Node 22, executed with Node 20 -> SIGSEGV
- ...

## Node.js Process Model
- `child_process.spawn()` `close` event receives `(code, signal)`
	- code is null when terminated by signal
- Unix exit code convention: 128+N = terminated by signal N
	- 139 = 128+11 = SIGSEGV
	- 137 = 128+9 = SIGKILL
- How parent process handles child exit code depends on implementation

## Node.js Abstraction Layers
- OS (Darwin) -> Node.js (V8 + libuv) -> Native Addons -> JavaScript
	- libuv: abstracts OS differences into a single async I/O model
	- V8: abstracts JS execution — interpreted, so safe across Node versions
	- Native Addon: links directly to V8 C++ ABI — binary incompatibility on version change
```

The test: if you have to mentally context-switch to read the new content after the existing content, it belongs under a separate `##`.

### Case 3: Not sure where it goes

Ask the user. A misplaced entry is harder to find later than a quick clarifying question now.

## Section patterns

Use nested bullets throughout — top-level states the headline, sub-bullets provide detail.

### Findings
```markdown
## Findings
- `path/to/file.ts:42` — what was found
	- Supporting detail or context
	- Pattern observed: [brief explanation]
- Key insight about [topic]
	- Evidence: [what backs this up]
```

### Analysis
```markdown
## Analysis
- **[Subject]**: [one-line summary]
	- Pro: ...
	- Con: ...
	- Verdict: ...
```

### Decisions
Every decision needs a "Why" — the rationale is more valuable than the choice itself.
```markdown
## Decisions
- **[Decision title]**: [what was decided]
	- Why: [the reasoning that led to this choice]
	- Alternative: [what else was considered and why it lost]
	- Trade-off: [what we're giving up]
```

### Debug

Debug entries are **command-first** — the user should be able to copy-paste the commands and reproduce the investigation months later. Prose explains the thinking between commands, not the other way around.

A complete debug entry has four parts:

1. **Symptom** — one bullet describing what went wrong
2. **Wrong turns** — what you tried that didn't work, and why it was wrong. This is the most valuable part for preventing future misdiagnoses
3. **Commands + results** — the actual investigation in a code block, with inline comments showing what each step revealed
4. **Checklist** — actionable "next time, do this first" items

```markdown
## Debug

### HH:MM — [short title]

- **Symptom**: [what happened — observable behavior]
- **Misdiagnosis**: [wrong hypothesis] -> [why it was wrong]
	- [what led you astray]
- **Root cause**: [the actual problem]

\```bash
# Step 1: [what you're checking and why]
<command>
# -> <result or exit code — the evidence>

# Step 2: [narrowing down — what variable you're isolating]
<command>
# -> <result>

# Step 3: [the fix]
<command>
# -> <verification that it worked>
\```

- **Lessons / check this first next time**:
	1. [most important thing to check first]
	2. [second thing]
	3. [third thing]
```

**Real example** (from a Node.js version mismatch debug session):

```markdown
### 16:10 — npm start silent exit

- **Symptom**: `npm start` prints "Build is up-to-date." then exits silently with no error
- **Misdiagnosis**: Suspected OAuth silent exit (#14943) or TTY loss (#13924)
	- Spent time analyzing code paths — turned out it wasn't a code issue at all
- **Root cause**: Artifacts built with Node 22, executed with Node 20 -> SIGSEGV

\```bash
# Step 1: check exit code — npm start swallows child process exit code
DEV=true node --no-warnings=DEP0040 packages/cli; echo "EXIT CODE: $?"
# -> EXIT CODE: 139 (SIGSEGV!)

# Step 2: isolate variables — disable one thing at a time to narrow down
DEV=true GEMINI_CLI_NO_RELAUNCH=true node packages/cli; echo "EXIT CODE: $?"
# -> 139 (not relaunch)
DEV=true GEMINI_CLI_NO_RELAUNCH=true GEMINI_SANDBOX=false node packages/cli; echo "EXIT CODE: $?"
# -> 139 (not sandbox) -> all 139 = build artifact issue

# Step 3: clean rebuild
nvm use 20.19.0 && npm run clean && npm install && npm run build
npm start  # -> works correctly
\```

- **Check this first next time**:
	1. `node --version` — verify it matches CONTRIBUTING.md requirements
	2. Silent exit -> check exit code first (139=SIGSEGV, 41=auth, 42=input)
	3. Suspect the environment before suspecting the code
```

### References
```markdown
## References
- [Issue title](url)
	- Why it matters: [one-liner context]
- [[Internal Note]]
	- Relevant because: [connection]
```

### Progress
```markdown
## Progress
- [x] Completed item
	- Outcome: [result or artifact]
- [ ] Remaining item
	- Blocked by: [dependency if any]
```
