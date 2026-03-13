#!/usr/bin/env python3
"""Extract YouTube transcript and metadata.

Transcript chain: defuddle (fastest, no rate limit) → yt-dlp → youtube-transcript-api.
Metadata: always yt-dlp (lightweight --print query, rarely rate-limited).
"""

import argparse
import random
import re
import subprocess
import sys
import tempfile
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path


# Tokens that indicate a transient, retryable error from any source.
_RETRY_TOKENS = (
    "429",
    "too many requests",
    "ratelimit",
    "rate limit",
    "temporar",
    "timed out",
    "timeout",
    "connection",
    "service unavailable",
    "server returned error",
    "unable to download webpage",
    "unexpected end of data",
    "internal server error",
)

_AUTO_LANG = "auto"

# Pre-compiled patterns used in the hot path of clean_srt().
_SRT_HTML_RE = re.compile(r"<[^>]+>")
_SRT_SEQ_RE = re.compile(r"^\d+$")
_SRT_TIME_RE = re.compile(r"^\d{2}:\d{2}:\d{2}")

_DEFUDDLE_TS_RE = re.compile(r"\*\*\d+:\d+\*\* · ")
_DEFUDDLE_ESCAPED_BRACKET_RE = re.compile(r"\\([\[\]])")

_FNAME_UNSAFE_RE = re.compile(r'[/\\:*?"<>|#^ㅣ]')
_FNAME_MULTI_SPACE_RE = re.compile(r" {2,}")


def sanitize_filename(title: str) -> str:
    """Remove characters Obsidian can't handle in wikilink filenames."""
    cleaned = _FNAME_UNSAFE_RE.sub("", title)
    return _FNAME_MULTI_SPACE_RE.sub(" ", cleaned).strip()


@dataclass(frozen=True)
class VideoMetadata:
    title: str
    channel: str
    channel_id: str
    upload_date: str  # ISO 8601 (YYYY-MM-DD) or empty string
    webpage_url_basename: str = ""  # "watch" for regular videos, "shorts" for Shorts


@dataclass(frozen=True)
class FetchConfig:
    max_retries: int = 4
    retry_base_seconds: int = 2
    sub_langs: tuple[str, ...] = ("ko", "en", _AUTO_LANG)  # mirrors CLI default "ko,en" + auto appended
    cookies_from_browser: str = ""
    no_fallback: bool = False
    force_api: bool = False
    timeout_metadata: int = 30
    timeout_subtitle: int = 60


def extract_video_id(url_or_id: str) -> str:
    patterns = [
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    print(f"Error: Could not extract video ID from: {url_or_id}", file=sys.stderr)
    sys.exit(1)


def run_cmd(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    """Run a command and always return a CompletedProcess for retry classification."""
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        timeout_msg = f"Command timed out after {timeout}s: {cmd}\n"
        merged_stderr = "\n".join(part for part in (stderr, timeout_msg) if part)
        return subprocess.CompletedProcess(cmd, 124, stdout, merged_stderr)


def _is_retryable_text(text: str) -> bool:
    """Return True if the text contains a token that signals a transient error."""
    lower = text.lower()
    return any(token in lower for token in _RETRY_TOKENS)


def is_retryable(obj: "subprocess.CompletedProcess | BaseException") -> bool:
    """Return True if a subprocess result or exception signals a transient error."""
    if isinstance(obj, subprocess.CompletedProcess):
        return _is_retryable_text(f"{obj.stdout}\n{obj.stderr}")
    return _is_retryable_text(str(obj))


def _backoff_delay(attempt: int, config: FetchConfig) -> float:
    """Exponential backoff with jitter: base * 2^attempt + uniform(0, 0.5)."""
    return config.retry_base_seconds * (2 ** attempt) + random.random() * 0.5


def _filter_non_auto_langs(langs: "tuple[str, ...] | list[str]") -> list[str]:
    """Return explicit (non-'auto') language codes, lowercased."""
    return [lang.lower() for lang in langs if lang and lang.lower() != _AUTO_LANG]


def execute_with_retries(
    cmd: list[str],
    timeout: int,
    config: FetchConfig,
    label: str,
) -> subprocess.CompletedProcess:
    """
    Retry wrapper for transient failures.
    Policy: exponential backoff + jitter, then fallback or error.
    """
    attempt = 0
    while True:
        result = run_cmd(cmd, timeout)
        if result.returncode == 0:
            if attempt:
                print(f"{label} succeeded after {attempt} retry attempt(s)", file=sys.stderr)
            return result

        if attempt >= config.max_retries:
            print(f"{label} retried {attempt} time(s) and failed", file=sys.stderr)
            return result
        if not is_retryable(result):
            return result

        sleep_seconds = _backoff_delay(attempt, config)
        print(
            f"{label} failed with transient error (attempt {attempt + 1}/{config.max_retries}), "
            f"retrying in {sleep_seconds:.1f}s",
            file=sys.stderr,
        )
        time.sleep(sleep_seconds)
        attempt += 1


def parse_sub_langs(raw_sub_langs: str) -> tuple[str, ...]:
    parsed = [lang.strip() for lang in raw_sub_langs.split(",") if lang.strip()]
    if not parsed:
        parsed = ["ko", "en"]
    if _AUTO_LANG not in parsed:
        parsed.append(_AUTO_LANG)
    return tuple(parsed)


def _subtitle_language(path: Path) -> str:
    """Extract the language code from a yt-dlp subtitle filename (e.g. sub.ko.srt → 'ko')."""
    match = re.search(r"\.([a-zA-Z-]+)\.srt$", path.name)
    return match.group(1).lower() if match else ""


def pick_srt_file(files: list[Path], preferred_langs: list[str]) -> Path:
    preferred = _filter_non_auto_langs(preferred_langs)
    lang_map = {path: _subtitle_language(path) for path in files}

    for lang in preferred:
        matching = [path for path in files if lang_map[path] == lang]
        if matching:
            return sorted(matching)[0]

    return sorted(files)[0]


def _format_upload_date(raw: str) -> str:
    """Convert yt-dlp YYYYMMDD date to ISO 8601 (YYYY-MM-DD). Returns empty string on invalid input."""
    raw = raw.strip()
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return ""


def fetch_metadata(video_id: str, config: FetchConfig) -> VideoMetadata:
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--print",
        "%(title)s\n%(channel)s\n%(channel_id)s\n%(upload_date)s\n%(webpage_url_basename)s",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    if config.cookies_from_browser:
        cmd.extend(["--cookies-from-browser", config.cookies_from_browser])

    result = execute_with_retries(
        cmd,
        timeout=config.timeout_metadata,
        config=config,
        label="yt-dlp metadata fetch",
    )

    if result.returncode != 0 or not result.stdout.strip():
        print("Warning: yt-dlp metadata failed, using fallback title.", file=sys.stderr)
        return VideoMetadata(title=video_id, channel="", channel_id="", upload_date="")

    parts = result.stdout.strip().splitlines()
    title, channel, channel_id, raw_date, url_basename = (parts + ["", "", "", "", ""])[:5]
    return VideoMetadata(
        title=title or video_id,
        channel=channel,
        channel_id=channel_id,
        upload_date=_format_upload_date(raw_date),
        webpage_url_basename=url_basename,
    )


def fetch_transcript_defuddle(video_id: str, config: FetchConfig) -> tuple[str, str]:
    """Tier 1: extract transcript via defuddle (fastest, no rate limiting)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    result = run_cmd(["defuddle", "parse", url, "--md"], timeout=config.timeout_subtitle)

    if result.returncode != 0:
        raise RuntimeError(f"defuddle failed: {result.stderr.strip()}")

    match = re.search(r"^## Transcript\s*\n(.+?)(?=^## |\Z)", result.stdout, re.DOTALL | re.MULTILINE)
    if not match:
        raise RuntimeError("defuddle: no ## Transcript section found")

    # Strip **H:MM** · timestamp prefixes, unescape brackets, collapse whitespace
    text = _DEFUDDLE_TS_RE.sub("", match.group(1))
    text = _DEFUDDLE_ESCAPED_BRACKET_RE.sub(r"\1", text)
    text = " ".join(text.split())

    if not text:
        raise RuntimeError("defuddle: transcript section was empty after cleaning")

    return text, "defuddle"


def fetch_transcript_ytdlp(video_id: str, config: FetchConfig) -> tuple[str, str]:
    """Tier 2: download SRT subtitles via yt-dlp."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--write-auto-sub",
            "--skip-download",
            "--sub-format",
            "srt",
            "--sub-langs",
            ",".join(config.sub_langs),
            "--retries",
            str(config.max_retries),
            "--retry-sleep",
            str(config.retry_base_seconds),
            "--sleep-interval",
            str(max(1, config.retry_base_seconds)),
            "-o",
            str(Path(tmpdir) / "sub"),
            f"https://www.youtube.com/watch?v={video_id}",
        ]
        if config.cookies_from_browser:
            cmd.extend(["--cookies-from-browser", config.cookies_from_browser])

        result = execute_with_retries(
            cmd,
            timeout=config.timeout_subtitle,
            config=config,
            label="yt-dlp transcript fetch",
        )
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp failed after retries: {result.stderr.strip()}")

        srt_files = sorted(Path(tmpdir).glob("*.srt"))
        if not srt_files:
            raise RuntimeError(f"yt-dlp: no subtitles found.\n{result.stderr.strip()}")

        subtitle_file = pick_srt_file(srt_files, list(config.sub_langs))
        srt_text = subtitle_file.read_text(encoding="utf-8-sig", errors="replace")
        lang_code = _subtitle_language(subtitle_file)

    return clean_srt(srt_text), lang_code


def fetch_transcript_api(video_id: str, config: FetchConfig) -> tuple[str, str]:
    """Fallback: youtube-transcript-api (pip install youtube-transcript-api)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:
        raise RuntimeError(
            "youtube-transcript-api not installed.\n"
            "Run: pip install youtube-transcript-api"
        ) from exc

    candidates = _filter_non_auto_langs(config.sub_langs) + [_AUTO_LANG]

    api = YouTubeTranscriptApi()
    last_error: Exception | None = None

    for lang in candidates:
        for attempt in range(config.max_retries + 1):
            try:
                if lang == _AUTO_LANG:
                    fetched = api.fetch(video_id)
                else:
                    fetched = api.fetch(video_id, languages=[lang])
                text = " ".join(s.text for s in fetched)
                if not text.strip():
                    raise RuntimeError("empty transcript payload")
                return text, lang
            except Exception as exc:
                last_error = exc
                if is_retryable(exc) and attempt < config.max_retries:
                    delay = _backoff_delay(attempt, config)
                    print(
                        f"youtube-transcript-api ({lang}) retryable error (attempt {attempt + 1}/{config.max_retries}), "
                        f"retrying in {delay:.1f}s",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                else:
                    break

    if last_error is None:
        last_error = RuntimeError("youtube-transcript-api returned no transcript")

    raise RuntimeError(
        "youtube-transcript-api: no transcript found. The video may be private, removed, "
        "or captions may be unavailable."
    ) from last_error


def fetch_transcript(video_id: str, config: FetchConfig) -> tuple[str, str]:
    """Chain: defuddle → yt-dlp → youtube-transcript-api."""
    if config.force_api:
        print("Using youtube-transcript-api only mode.", file=sys.stderr)
        return fetch_transcript_api(video_id, config)

    # Tier 1: defuddle (fastest, no rate limiting)
    try:
        return fetch_transcript_defuddle(video_id, config)
    except Exception as exc:
        print(f"defuddle failed ({type(exc).__name__}): {exc}", file=sys.stderr)

    # Tier 2: yt-dlp (SRT subtitles)
    try:
        return fetch_transcript_ytdlp(video_id, config)
    except Exception as exc:
        if config.no_fallback:
            raise
        print(f"yt-dlp failed ({type(exc).__name__}): {exc}", file=sys.stderr)

    # Tier 3: youtube-transcript-api
    print("Falling back to youtube-transcript-api...", file=sys.stderr)
    return fetch_transcript_api(video_id, config)


def clean_srt(srt: str) -> str:
    """Strip SRT sequence numbers, timestamps, HTML tags, and deduplicate overlapping lines."""
    srt = _SRT_HTML_RE.sub("", srt)
    lines = srt.split("\n")
    text_lines = []
    for line in lines:
        line = line.strip()
        if _SRT_SEQ_RE.match(line):
            continue
        if _SRT_TIME_RE.match(line):
            continue
        if line:
            text_lines.append(line)

    # Sliding-window dedup (maxlen=6) removes locally overlapping subtitle segments,
    # which yt-dlp auto-subs often emit for the same spoken text across adjacent timestamps.
    deduped = []
    seen: deque[str] = deque(maxlen=6)
    for line in text_lines:
        if line not in seen:
            deduped.append(line)
        seen.append(line)

    return " ".join(deduped)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract YouTube transcript via defuddle / yt-dlp / youtube-transcript-api"
    )
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--max-retries", type=int, default=4, help="Maximum retry attempts for transient failures")
    parser.add_argument("--sub-langs", default="ko,en", help="Preferred subtitle languages")
    parser.add_argument("--retry-base-seconds", type=int, default=2, help="Base seconds for exponential backoff")
    parser.add_argument("--cookies-from-browser", default="", help="Pass to yt-dlp --cookies-from-browser")
    parser.add_argument("--no-fallback", action="store_true", help="Skip youtube-transcript-api fallback")
    parser.add_argument("--prefer-api", action="store_true", help="Use youtube-transcript-api only")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    config = FetchConfig(
        max_retries=args.max_retries,
        retry_base_seconds=args.retry_base_seconds,
        sub_langs=parse_sub_langs(args.sub_langs),
        cookies_from_browser=args.cookies_from_browser,
        no_fallback=args.no_fallback,
        force_api=args.prefer_api,
    )

    meta = fetch_metadata(video_id, config)

    # Shorts guard — exit before any transcript work.
    # yt-dlp resolves webpage_url_basename to "shorts" for Shorts, "watch" for regular videos.
    if meta.webpage_url_basename == "shorts":
        print("Skipped: YouTube Shorts are not clipped.", file=sys.stderr)
        sys.exit(2)

    try:
        body, lang_code = fetch_transcript(video_id, config)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    header = (
        f"# {meta.title}\n"
        f"Channel: {meta.channel} | ChannelID: {meta.channel_id} | Date: {meta.upload_date}\n"
        f"Sanitized-Title: {sanitize_filename(meta.title)}\n\n"
    )
    output = header + body

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Saved to {args.output} ({lang_code}, {len(body)} chars)")
    else:
        print(output)


if __name__ == "__main__":
    main()
