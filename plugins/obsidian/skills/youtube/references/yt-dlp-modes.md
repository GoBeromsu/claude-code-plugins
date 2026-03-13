# yt-dlp Mode Reference

Reference for any skill that invokes yt-dlp, particularly `/fyc` (channel discovery)
and `/youtube` (transcript extraction).

## Mode Comparison

| Mode | Flag | Speed | `upload_date` | `--dateafter` | Use case |
|------|------|-------|---------------|---------------|----------|
| Flat-playlist | `--flat-playlist` | Fast (no HTTP per video) | **NA — unavailable** | Ignored | Bulk URL listing only |
| Default (full metadata) | _(no flag)_ | Slow (1 HTTP req per video) | Available (`YYYYMMDD`) | Works correctly | Date filtering, metadata needed |

**Key rule**: `--dateafter` is silently ignored in `--flat-playlist` mode — it returns the entire playlist archive instead of filtering. Never combine the two for date-based filtering.

## Common Patterns

### List recent video URLs (no date needed)
```bash
yt-dlp --flat-playlist \
       --print "%(webpage_url)s" \
       --playlist-end 20 \
       --no-warnings \
       "<channel_url>/videos"
```

### Get dates for N most recent videos
```bash
yt-dlp --playlist-end 10 \
       --print "%(upload_date)s %(webpage_url)s" \
       --no-warnings \
       "<channel_url>/videos"
# upload_date format: YYYYMMDD
```

### Filter by date (correct way)
```bash
# Option A — RSS feed (fastest, no yt-dlp, max 15 videos)
today=$(date +%Y-%m-%d)
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<UCxxxxx>" \
  | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
ns_yt   = '{http://www.youtube.com/xml/schemas/2015}'
ns_atom = '{http://www.w3.org/2005/Atom}'
today = sys.argv[1]
for entry in tree.findall(f'{ns_atom}entry'):
    vid = entry.find(f'{ns_yt}videoId').text
    pub = entry.find(f'{ns_atom}published').text[:10]
    if pub == today:
        print(f'https://www.youtube.com/watch?v={vid}')
" "$today"

# Option B — yt-dlp full metadata (slower, no video limit)
yt-dlp --dateafter 20260224 \
       --print "%(webpage_url)s" \
       --no-warnings \
       "<channel_url>/videos"

# Option C — yt-dlp, check first N only (fast enough for low-frequency channels)
yt-dlp --playlist-end 5 \
       --print "%(upload_date)s %(webpage_url)s" \
       --no-warnings \
       "<channel_url>/videos" \
  | awk -v today="$(date +%Y%m%d)" '$1 == today {print $2}'
```

## Resolving Channel Handle → Channel ID

RSS feed requires `channel_id` (`UCxxxxxxxxxxxxxxxxxxxxxxxx`), not a handle (`@name`).

```bash
# Resolve once, then cache in the People note (youtube_channel_id property)
yt-dlp --playlist-end 1 \
       --print "%(channel_id)s" \
       --no-warnings \
       "https://www.youtube.com/@handle" 2>/dev/null | head -1
```

## Field Availability Summary

Fields available in `--flat-playlist` mode (incomplete — dates are NOT available):
- `%(webpage_url)s` ✓
- `%(id)s` ✓
- `%(title)s` ✓ (sometimes)
- `%(upload_date)s` ✗ → always `NA`
- `%(duration)s` ✗ → always `NA`

Fields available in default (full metadata) mode:
- All of the above ✓
- `%(upload_date)s` ✓ — format `YYYYMMDD`
- `%(duration)s` ✓
- `%(description)s` ✓
- `%(channel_id)s` ✓
