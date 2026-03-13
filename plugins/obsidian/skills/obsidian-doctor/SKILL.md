---
name: obsidian-doctor
description: >
  Diagnose and fix stale/broken paths across Obsidian vault configs, plugins,
  templates, and note content after folder restructuring. Use when: user invokes
  /obsidian-doctor, says 'vault check', 'plugin path check', 'stale path scan',
  'config check', 'vault sanity check', 'broken path', or after any folder
  rename/move/restructuring operation. Also use proactively after bulk vault
  operations. NOT for note content editing. NOT for infrastructure/sync issues
  (use obsidian-sync).
---

# obsidian-doctor

Automated vault health checker that detects and fixes stale folder paths across plugin configs, core configs, templates, guidelines, and note content. Runs a diagnose-fix-verify loop until the vault is clean.

## When to Use

- After folder renames, moves, or restructuring
- When plugins behave unexpectedly after vault changes
- Periodic vault health checks
- User says: `/obsidian-doctor`, `vault check`, `config check`, `stale path`, `broken path`

## Input

The skill accepts optional old->new path mappings. If none provided, it auto-detects by comparing config paths against actual folder structure.

```
# Examples:
/obsidian-doctor
/obsidian-doctor "Old Folder" -> "New Folder", "Another/Old" -> "Another/New"
```

## Workflow

### Phase 1: Diagnose

**Goal**: Build a complete list of stale paths across the vault.

1. **Inventory actual folders**:
```bash
# List top-level vault folders
ls -d */ | head -30

# Or via Obsidian CLI if available (replace <VAULT_NAME> with your vault name)
obsidian eval "app.vault.getAbstractFileByPath('/').children.filter(f => f.children).map(f => f.path)" vault=<VAULT_NAME>
```

2. **Scan configs for path references**:
```bash
# Plugin configs — adjust the numbered prefix pattern to match your vault's folder naming convention
grep -r "00\.\|10\.\|20\.\|30\.\|40\.\|50\.\|60\.\|70\.\|80\.\|90\." .obsidian/ --include="*.json" -l

# Templates and guidelines — adjust paths to your vault's template/config directories
grep -rl "00\.\|10\.\|20\.\|30\.\|40\.\|50\.\|60\.\|70\.\|80\.\|90\." <TEMPLATE_DIR>/ <CONFIG_DIR>/ 2>/dev/null
```

3. **Cross-reference**: For each path found in configs, check if the folder actually exists. Paths referencing non-existent folders = stale.

4. **Accept user input**: If the user provided old->new mappings, add those to the stale path list.

5. **Present findings** to user:
```
Found N stale paths across M files:
- "Old Folder/" -> referenced in 12 files (folder does not exist, likely renamed to "New Folder/")
- "Another/Old/" -> referenced in 3 files (folder does not exist)
```

Wait for user confirmation before proceeding to Phase 2. If zero stale paths found, skip to Phase 3 (verify-only mode).

### Phase 2: Fix (Parallel Agents)

Launch 5 agents in parallel. Each agent:
- Reads the reference file at `references/plugin-paths.md` (relative to this skill)
- Receives the stale->correct path mapping from Phase 1
- Fixes all occurrences in its domain
- Reports back: `{files_changed: [], changes_made: N}`

| Agent | subagent_type | Domain | Files |
|-------|---------------|--------|-------|
| **config-doctor** | `general-purpose` | Plugin configs | `.obsidian/plugins/*/data.json` |
| **core-doctor** | `general-purpose` | Core Obsidian configs | `.obsidian/*.json` (workspace, workspaces, hotkeys, templates, bookmarks, webviewer) |
| **template-doctor** | `general-purpose` | Templates & prompts | Your vault's template and prompt directories |
| **guideline-doctor** | `general-purpose` | Guidelines & agent configs | Your vault's guideline directories, `.claude/` configs |
| **content-doctor** | `general-purpose` | Vault note content | All `.md` files -- wikilinks, embeds, image paths, inline folder refs |

**Agent prompt template** (customize per domain):
```
You are obsidian-doctor's {name} agent.

Task: Fix stale folder paths in {domain}.

Stale->Correct mappings:
{mappings}

Reference: Read the plugin-paths.md reference file for which fields contain paths.

Scope: Only modify files in {file_scope}.
Method: Use Read to inspect, Edit to fix. For bulk replacements across many files, use Bash with sed.
Report: List every file changed and total changes made.

IMPORTANT:
- Only replace exact path matches (avoid partial substring matches)
- Preserve JSON structure -- validate after editing
- For wikilinks: [[old/path/note]] -> [[new/path/note]] (but most wikilinks don't include paths -- only fix those that do)
- Do NOT modify .obsidian/plugins/*/main.js or manifest.json
```

### Phase 3: Verify (Loop Until Clean)

This is the critical phase. First-pass fixes always miss some paths.

**Loop**:
1. **Sweep** for remaining stale paths:
```bash
# Build grep pattern from all stale paths
grep -rl "stale-path-1\|stale-path-2" .obsidian/ <TEMPLATE_DIR>/ <CONFIG_DIR>/ --include="*.json" --include="*.md"
```

2. **If hits found**: Spawn targeted fix agents for the specific files -> re-sweep.

3. **If clean**: Exit loop and proceed to validation.

**Validation checks** (run in parallel):
```bash
# 1. Reload Obsidian to pick up config changes (if Obsidian CLI available)
obsidian reload vault=<VAULT_NAME>

# 2. Verify folder structure
obsidian eval "app.vault.getAbstractFileByPath('/').children.filter(f => f.children).map(f => f.path)" vault=<VAULT_NAME>

# 3. Check broken wikilinks
obsidian links --broken vault=<VAULT_NAME>

# 4. (Optional) Reindex search — if using a search indexer like qmd, omnisearch, etc.
# qmd update && qmd embed
```

### Phase 4: Report

Present a summary table:

```
## Obsidian Doctor Report

### Stale Paths Fixed
| Old Path | New Path | Files Fixed |
|----------|----------|-------------|
| Old Folder/ | New Folder/ | 14 |
| Another/Old/ | Another/New/ | 3 |

### Domain Summary
| Domain | Files Changed | Changes Made |
|--------|--------------|--------------|
| Plugin configs | 5 | 8 |
| Core configs | 3 | 12 |
| Templates | 2 | 4 |
| Guidelines | 4 | 6 |
| Note content | 3 | 5 |

### Remaining Issues
- [if any] Bookmarks referencing deleted files (user decision needed)
- [if any] cursor-positions.json stale entries (low priority, auto-cleaned by Obsidian)

### Next Steps
- [ ] Monitor Obsidian Sync for ghost folder recreation on remote
- [ ] Run `obsidian links --broken` again after sync completes
```

## Edge Cases

- **JSON validity**: After editing `data.json` files, validate JSON structure. If broken, restore from the pre-edit content.
- **Partial path matches**: `"10. Time"` should not match `"10. Time/01. Calendar"` when replacing -- use exact path boundaries.
- **Wikilinks without paths**: Most wikilinks are just `[[Note Title]]` without folder paths. Only fix wikilinks that explicitly include folder paths like `[[Old Folder/Some Note]]`.
- **Escaped paths in JSON**: Paths in JSON may have escaped characters. Match both raw and escaped forms.
- **cursor-positions.json**: Contains per-file cursor state. Stale entries here are harmless -- Obsidian auto-cleans them. Low priority fix.
- **workspace.json lastOpenFiles**: Stale entries cause no errors but clutter the recent files list. Fix these.
