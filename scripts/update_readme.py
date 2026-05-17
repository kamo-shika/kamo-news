# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""news/ の Markdown を走査し、README.md の「最新記事」セクションを再生成する."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
MARKER_START = "<!-- LATEST:START -->"
MARKER_END = "<!-- LATEST:END -->"


def find_news_files(news_dir: Path) -> list[Path]:
    files = [p for p in news_dir.iterdir() if DATE_PATTERN.match(p.name)]
    return sorted(files, key=lambda p: p.name, reverse=True)


def extract_title(md_path: Path) -> str:
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def render_latest_section(news_dir: Path, limit: int) -> str:
    files = find_news_files(news_dir)[:limit]
    lines = [f"- [{extract_title(f)}](news/{f.name})" for f in files]
    return "\n".join(lines) if lines else "_まだ記事がありません。_"


def update_readme(readme_path: Path, news_dir: Path, limit: int) -> None:
    content = readme_path.read_text(encoding="utf-8")
    if MARKER_START not in content or MARKER_END not in content:
        raise ValueError(f"README is missing markers: {MARKER_START} / {MARKER_END}")

    section = render_latest_section(news_dir, limit)
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL,
    )
    replacement = f"{MARKER_START}\n{section}\n{MARKER_END}"
    new_content = pattern.sub(replacement, content)
    readme_path.write_text(new_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--news-dir", default="news")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    update_readme(Path(args.readme), Path(args.news_dir), args.limit)


if __name__ == "__main__":
    main()
