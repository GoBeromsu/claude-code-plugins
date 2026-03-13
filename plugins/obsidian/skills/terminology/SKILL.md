---
name: terminology
description: >
  Create, rewrite, and consolidate PKM terminology notes in
  70. Collections/72. Terminologies/. Handles variant detection across the vault,
  boilerplate cleanup ("기존 노트 필기" absorption), and duplicate merging via obsidian CLI.
  Use when: (1) /terminology, (2) "용어 노트 만들어줘" or "노트 만들어줘" for a concept,
  (3) user learned a term and wants to document it, (4) "검색해보고 노트 만들어줘",
  (5) user wants to consolidate duplicate notes about a concept.
  Do NOT use for general document writing — use the docs skill instead.
---

# terminology

## Core Principles

- **Vault over web**: personal insights and vault notes take priority over external sources
- **No fabrication**: every wikilink must be confirmed by qmd; every URL must be confirmed via defuddle — never invent DOIs
- **obsidian CLI first**: use `obsidian` CLI for vault mutations (delete, rename, property:set) — safer than raw filesystem ops
- **Single note output**: produce one terminology note; do NOT modify neighboring notes

## Filename

1. Has common acronym → `Full English Term (ACRONYM).md`
2. No acronym → `English Term (Korean).md`

## Creation Process

### Step 1: Assess

Run a five-pronged variant scan (all in parallel):
```
1. Glob: **/*[term]*                            — filename matches
2. qmd query: lex "[term]" + vec "[term]"       — content/semantic matches
3. obsidian backlinks file="[term]"             — existing wikilink references
4. obsidian search query="[term]"               — Obsidian index search (catches alias-resolved matches)
5. Grep: "\[\[.*[term].*\]\]"                   — exact wikilink pattern matches across vault
```

Classify each found note by reading it:

| Type | Signal | Action |
|---|---|---|
| Empty stub | Only frontmatter, no body | Add filename to canonical `aliases` → `obsidian delete` |
| Boilerplate | "정합성을 위해", "상호참조 항목" | Discard auto-generated sections |
| Has 기존 노트 필기 | `## 기존 노트 필기` header present | **Priority source** — absorb hand-written content below header |
| Real content | Hand-written, specific insights | Read fully, merge into draft |

**Canonical location**: `70. Collections/72. Terminologies/[Filename Convention].md`

| Context | Action |
|---|---|
| Source material provided | Extract directly; skip WebSearch |
| Personally defined | Vault search only; skip WebSearch |
| Term only, no existing notes | Run Step 2 in full |
| Note(s) found | **Merge** — read all variants fully before continuing |

### Step 2: Research

Run all applicable branches in parallel:

**WebSearch** (skip if source provided or personally defined):
```
"[TERM] definition mechanism application"
```
Run **defuddle** on promising URLs for deep extraction.

**Vault search** (always run, both in parallel):
```bash
qmd query: lex "[English term]" -n 15
qmd query: lex "[Korean variant]" -n 15
```

**Personal experience scan** — from results, flag personal notes (journals, CMDs, dated entries):
- Read top 2–3 flagged files; extract the personal connection to the concept

### Step 3: Draft

Read `references/template.md` for frontmatter schema, body structure, and citation rules.

**When existing note has "기존 노트 필기" pattern:**
1. **Discard** all auto-generated content above the header (boilerplate markers: "정합성을 위해 기초 근거를 정리한다", "개념적 경계가 겹치는 상호참조 항목", placeholder "빌더 직관" TL;DR that just restates the definition)
2. **Absorb** hand-written content below `## 기존 노트 필기` — Literature Review entries, code examples, Related Concepts with real descriptions
3. **Remove** the "기존 노트 필기" header — restructure content into proper template sections

**Draft structure:**

1. **Definition block**: one paragraph + 2–4 key characteristics
2. **Literature Review** (≥2 entries):
   - Opening per entry: natural Korean — why this source, what unique delta it adds; no fixed template
   - Body: claim-tree, max depth 3; LaTeX where it clarifies
3. **Personal Insights** (always present — never skip):
   - Personal notes found → `### [[VaultNoteTitle]]` + free-form body (prose, bullets, blockquotes)
4. **Related Concepts**: wikilinks only
   - Verify each: `qmd query: lex "[Term]" -n 3`
   - Not found → plain text, never fabricate

### Step 4: Verify

- [ ] Frontmatter: `aliases`, `moc`, `date_created`, `date_modified`, `tags` (PascalCase + `terminology`), `type`
- [ ] TL;DR: insight or trade-off, not a definition restatement
- [ ] Literature Review: ≥2 entries, each opening = natural Korean delta (no formula)
- [ ] `## Personal Insights` present (entries or placeholder)
- [ ] All wikilinks qmd-verified; all external URLs defuddle-confirmed
- [ ] `Related Concepts` section present
- [ ] No boilerplate phrases remain ("정합성을 위해", "상호참조 항목")

### Step 5: Publish

**Write the note**: Use `Write` tool to create/overwrite at canonical path.

**Variant cleanup** (for each non-canonical variant found in Step 1):
1. Add variant filename (sans `.md`) to canonical note's `aliases` in frontmatter
2. Delete the variant (parallel OK if multiple):
```bash
obsidian delete file="VariantName"
```
3. `[[OldName]]` wikilinks now auto-resolve via Obsidian alias resolution

**Re-index:**
```bash
qmd update && qmd embed
```
