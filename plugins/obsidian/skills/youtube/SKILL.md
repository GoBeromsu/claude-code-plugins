---
name: youtube
description: >-
  Extract a YouTube transcript and convert it into a Korean article clipping
  saved to the Obsidian vault. Use whenever the user provides a YouTube URL
  (youtube.com/watch, youtu.be, or /shorts/) and wants to clip, save, read, or
  summarize it — including Korean requests like "클리핑해줘", "내용 정리해줘",
  "vault에 저장해줘", or "한국어 기사로 만들어줘". Also use when the user provides an
  existing clipping filename that needs reprocessing because it still contains
  raw timestamped lines (e.g. "타임스탬프 라인이 남아있어", "재처리해줘"). Do NOT use for
  non-YouTube platforms (Vimeo, TikTok), channel discovery (/fyc), or requests
  to just summarize an already-processed clipping. Triggers on /youtube, any
  YouTube URL with clip/save/read intent, or clipping files needing reprocessing.
---

# YouTube Transcript → Article Clipping

## Goal

Speech-to-text rewriting, not summarization. Every sentence the speaker said
must appear in the output — rewritten as written prose (문어체), with only
filler words and stutters removed. Examples, anecdotes, data, and Q&A exchanges
are preserved verbatim in rewritten form.

## Workflow

### 0. Shorts guard

Shorts detection is handled automatically inside `transcript.py` — no separate step needed. The script fetches `%(webpage_url_basename)s` from yt-dlp alongside other metadata; if the value is `"shorts"`, it exits with code `2` and prints `"Skipped: YouTube Shorts are not clipped."` to stderr. Treat exit code `2` as a clean skip, not an error.

### 1. Extract transcript

```bash
SKILL_DIR=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)
python3 "$SKILL_DIR/scripts/transcript.py" '<url>' \
  -o /tmp/yt_transcript_<video_id>.txt
```

`SKILL_DIR` resolves to the `youtube/` skill directory relative to the running script.

Parse from output file header:
- Line 1: `# <title>` — raw title; use inside the note body (YAML, H1 heading)
- Line 2: `Channel: <channel> | ChannelID: <channel_id> | Date: <upload_date>` (`upload_date` is in `YYYYMMDD` format — convert to `YYYY-MM-DD` for YAML)
- Line 3: `Sanitized-Title: <sanitized_title>` — use this as the output filename (script strips `/ \ : * ? " < > | # ^ ㅣ` and collapses spaces)

### 2. ICT via subagent

For every video (single or multiple), spawn one `general-purpose` subagent per video in the same turn. The main context's only job after this point is to wait for results and report.

Each subagent receives:
- Transcript file path (`/tmp/yt_transcript_<video_id>.txt`)
- Video URL, title, channel display name, channel ID, upload date
- Output path (`80. References/86. Videos/<sanitized_title>.md`)
- Reprocessing flag (true if file already exists with raw transcript)
- The full ICT instruction below (Phases 0–4)

Report on completion: "N/M videos processed" with per-video status.

---

#### ICT (chunked multi-turn) — runs inside subagent

**Phase 0 — Author resolution only**:

Map the channel to a vault People note using the channel ID:

```bash
obsidian search "youtube_channel_id: <channel_id>"   # exact property match
```

- If a People note is found, record `author_link = "[[<note_filename>]]"` — use the note's filename, not the YouTube display name
- If no match, record `author_link = "[[<channel_display_name>]]"` as a fallback
- The channel display name and vault note name are intentionally separate — don't conflate them
- **Never** embed a pipe alias inside a YAML value without double-quoting it

Do NOT search for entities yet — that happens after the full text is written (Phase 4).

**Phase 1 — Split & Outline**:

```bash
CHUNK_FILES=$(python3 "$SKILL_DIR/scripts/split_transcript.py" /tmp/yt_transcript_<video_id>.txt)
```

Capture stdout — `split_transcript.py` prints one chunk file path per line. Read all chunk files listed in `$CHUNK_FILES`. Create a chapter outline:
- 1 chapter per ~500-800 transcript words (3-12 total, cap 12)
- Merge any cluster < 200 words into neighbor
- Each heading: specific Korean topic description

**Phase 2 — Skeleton**:

Determine the output path now: `80. References/86. Videos/<sanitized_title>.md`. Write the skeleton clipping file to that path with YAML + embed + placeholder TL;DR + placeholder Summary + `## 강의 전문` + all `###` chapter headings with `<!-- ICT:PENDING -->` markers.

**Phase 3 — Per-chapter fill** (sequential Edit calls):

For each chapter in order, one Edit replacing `<!-- ICT:PENDING -->`:
- Convert corresponding transcript segment to Korean written prose (문어체)
- **Every sentence must appear** — rewrite, don't omit. This is the whole point.
- Remove only filler/stutters; preserve examples, anecdotes, data, Q&A verbatim
- End with complete sentence + proper punctuation
- After each chapter's prose, append a mermaid diagram visualizing the key concept. Use `/obsidian-mermaid` skill rules. Choose the best diagram type (flowchart, sequence, mindmap, state). Cap at 5 nodes. If a mermaid block already exists, replace it.

**Long video handling** (3+ chunk files): Process one chunk file at a time — read a chunk, rewrite the corresponding chapter(s), Edit into skeleton, then move to the next chunk. Never attempt to hold the full transcript in working memory at once.

**Phase 4 — Entity scan & wikilinks** (after full text is written):

Now that the prose is complete, extract up to 15 key linkable entities (people, concepts, terms, methodologies) from the finished article. Search for each candidate using:
- `qmd` — search vault for matching notes
- `obsidian search query="<term>"` — confirm real filename

Build a wikilink lookup table and apply links via Edit (first occurrence per entity):
```
에이전틱 → [[Agentic AI|에이전틱]]
트랜스포머 → [[Transformer (트랜스포머)|트랜스포머]]
```
- Cap at 15 entities to avoid excessive CLI calls
- Skip generic words that would over-link (e.g. "데이터", "기술")
- This phase should complete within 2 minutes — if searches are slow, proceed with whatever you have

Also in this phase:
- Replace TL;DR placeholder: 1-sentence sharp insight
- Replace Summary placeholder: X-style catchy summary

### 3. Sanity check

- No `<!-- ICT:PENDING -->` markers remain
- Each chapter body is non-empty (chapters from short transcript segments may have 1–2 paragraphs — acceptable if the source is brief)
- Last sentence ends with proper punctuation (not cut off mid-sentence)
- Each major topic thread in transcript has a corresponding `###` section
- If truncated: set `status: reviewed`, never `done`
- Korean spoken → written prose compresses naturally; character ratio alone is not a valid completeness check

### 4. Write clipping

Output path: `80. References/86. Videos/<sanitized_title>.md`

Document structure (in order):

```
[YAML]
[YouTube embed]
> [!abstract] TL;DR
> [1-sentence essential insight]

## 공명                          ← reprocessing only; omit for new clippings
[#### subsections within 공명]

## Summary
[X-style catchy summary]

## 강의 전문 (or ## Transcript)
### Chapter 1 ...
[ICT-processed prose]
```

```yaml
---
author: ["<author_link>"]
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
image: "https://img.youtube.com/vi/<video_id>/maxresdefault.jpg"
review: "[[<sanitized_title>.review]]"
source: "<youtube url>"
speaker: []
status: done
type: video
tags: [reference, reference/video]
---
```

`<author_link>` is resolved in Phase 0. Use the People note name if found (`[[BZCF]]`), otherwise the channel display name (`[[비즈까페]]`). The surrounding `"..."` in YAML ensures any `|` characters inside wikilinks don't break YAML parsing.

`speaker`: fill if identifiable, otherwise leave empty.

### Reprocessing existing clippings

When the target file already exists:

1. **Read the file first** — identify personal content scattered across sections (`## 공명`, `## Thinking`, `## Linking`, `## Summary` subsections like Analogy/Insights, user notes, personal callouts)
2. **Consolidate into `## 공명`** — move all personal content under a single `## 공명` section; demote their headings to `####` subsections within it (e.g. `#### Linking`, `#### 💡 Insights`); remove the now-empty `## Linking`, `## Summary`, `## Thinking` shells
3. **Replace only** the raw transcript section (lines with `- HH:MM timestamps`) and any skeleton ICT sections
4. Keep existing YAML fields; only add missing ones (`status`, `speaker`, `review`)
5. Existing mermaid blocks will be replaced during Phase 3 (ICT agent handles mermaid inline)

## Multiple URLs

Extract all transcripts in parallel first (one Bash call each), then follow the same subagent-per-video flow described in §2. There is no separate code path for multiple URLs — the §2 architecture handles 1 or N identically.

## Error Handling

- No captions / private video → skip + report
- Clipping already exists + raw transcript → reprocess, preserving personal sections (see above)
- Truncation detected → `status: reviewed`

## Notes

- Transcript extraction uses a 3-tier fallback chain: defuddle (fastest, no rate limit) → yt-dlp → youtube-transcript-api
- Requires `defuddle` (`npm install -g defuddle`) and `yt-dlp` (`brew install yt-dlp`); no venv or extra deps needed
- Accepts full YouTube URLs, youtu.be, shorts, or bare 11-char video IDs
- For yt-dlp mode behavior (flat-playlist limitations, date filtering patterns, RSS alternative): see `references/yt-dlp-modes.md`
