"""Convert YouTube auto-sub VTT files into case-study folders with transcript.txt.

Usage: vtt_to_transcript.py SUBS_DIR SLUGS_JSON
SUBS_DIR holds <id>.en.vtt files; SLUGS_JSON maps video id -> folder name.
"""
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def vtt_to_text(vtt: str) -> str:
    kept: list[str] = []
    for line in vtt.splitlines():
        if not line.strip() or "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        # Auto-subs repeat the previous caption line at the start of each cue.
        if line and (not kept or kept[-1] != line):
            kept.append(line)
    text = re.sub(r"\s+", " ", " ".join(kept)).strip()
    return textwrap.fill(text, width=100) + "\n"


def main() -> None:
    subs_dir = Path(sys.argv[1])
    slugs = json.loads(Path(sys.argv[2]).read_text())
    for video_id, folder in slugs.items():
        vtt = subs_dir / f"{video_id}.en.vtt"
        if not vtt.exists():
            print(f"missing subtitles: {video_id}")
            continue
        out = ROOT / folder / "transcript.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text(vtt_to_text(vtt.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
