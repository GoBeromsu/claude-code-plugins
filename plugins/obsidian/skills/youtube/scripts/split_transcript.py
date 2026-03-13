#!/usr/bin/env python3
"""Split a YouTube transcript file into ~1500-word chunks at sentence boundaries."""

import re
import sys
from pathlib import Path


def split_into_sentences(text: str) -> list[str]:
    """Split text at sentence boundaries (. ! ? followed by space/newline/EOF).
    Falls back to individual words when punctuation is absent (e.g. Korean auto-captions)."""
    parts = re.split(r'(?<=[.!?])\s+', text)
    parts = [s.strip() for s in parts if s.strip()]
    if len(parts) > 5:
        return parts
    return text.split()


def chunk_words(words: list[str], target_words: int) -> list[str]:
    """Batch individual words into chunks of target_words (joined by spaces)."""
    return [
        " ".join(words[i : i + target_words])
        for i in range(0, len(words), target_words)
    ]


def chunk_sentences(sentences: list[str], target_words: int = 1500) -> list[list[str]]:
    """Group sentences into chunks of approximately target_words words.
    When each 'sentence' is a single word (Korean fallback), delegates to
    chunk_words() to avoid redundant per-word split() calls."""
    if sentences and " " not in sentences[0] and (len(sentences) < 2 or " " not in sentences[1]):
        return [[chunk] for chunk in chunk_words(sentences, target_words)]

    chunks: list[list[str]] = []
    current: list[str] = []
    current_words = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current and current_words + word_count > target_words:
            chunks.append(current)
            current = [sentence]
            current_words = word_count
        else:
            current.append(sentence)
            current_words += word_count

    if current:
        chunks.append(current)

    return chunks


def main():
    if len(sys.argv) < 2:
        print("Usage: split_transcript.py <transcript_file>", file=sys.stderr)
        sys.exit(1)

    transcript_path = Path(sys.argv[1])
    if not transcript_path.exists():
        print(f"Error: {transcript_path} not found", file=sys.stderr)
        sys.exit(1)

    text = transcript_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Skip header block (everything before the first blank line).
    # Header format is produced by transcript.py: title, channel, sanitized-title, blank.
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            body_start = i + 1
            break

    body = "\n".join(lines[body_start:]).strip()

    if not body:
        print(f"Error: transcript body is empty after header removal: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    # Extract video_id from filename pattern: yt_transcript_<video_id>.txt
    video_id = transcript_path.stem.removeprefix("yt_transcript_")

    sentences = split_into_sentences(body)
    chunks = chunk_sentences(sentences, target_words=1500)

    output_dir = transcript_path.parent
    for i, chunk in enumerate(chunks, start=1):
        chunk_text = " ".join(chunk)
        chunk_path = output_dir / f"yt_chunk_{video_id}_{i:03d}.txt"
        chunk_path.write_text(chunk_text, encoding="utf-8")
        print(str(chunk_path))


if __name__ == "__main__":
    main()
