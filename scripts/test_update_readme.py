"""update_readme.py の単体テスト."""

from pathlib import Path

import pytest

from update_readme import (
    extract_title,
    find_news_files,
    render_latest_section,
    update_readme,
)


def test_find_news_files_sorted_desc(tmp_path: Path) -> None:
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    (news_dir / "2026-05-15.md").write_text("# AI トレンドニュース 2026-05-15\n")
    (news_dir / "2026-05-17.md").write_text("# AI トレンドニュース 2026-05-17\n")
    (news_dir / "2026-05-16.md").write_text("# AI トレンドニュース 2026-05-16\n")
    (news_dir / ".gitkeep").write_text("")

    files = find_news_files(news_dir)

    assert [f.name for f in files] == [
        "2026-05-17.md",
        "2026-05-16.md",
        "2026-05-15.md",
    ]


def test_find_news_files_ignores_non_date_files(tmp_path: Path) -> None:
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    (news_dir / "2026-05-17.md").write_text("# x\n")
    (news_dir / "README.md").write_text("# x\n")
    (news_dir / "draft.md").write_text("# x\n")

    files = find_news_files(news_dir)

    assert [f.name for f in files] == ["2026-05-17.md"]


def test_extract_title_from_h1(tmp_path: Path) -> None:
    md = tmp_path / "2026-05-17.md"
    md.write_text("# AI トレンドニュース 2026-05-17\n\n本文\n")

    assert extract_title(md) == "AI トレンドニュース 2026-05-17"


def test_extract_title_fallback_to_filename(tmp_path: Path) -> None:
    md = tmp_path / "2026-05-17.md"
    md.write_text("本文のみ\n")

    assert extract_title(md) == "2026-05-17"


def test_render_latest_section_limits_to_n(tmp_path: Path) -> None:
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    for day in range(1, 11):
        (news_dir / f"2026-05-{day:02d}.md").write_text(
            f"# AI トレンドニュース 2026-05-{day:02d}\n"
        )

    section = render_latest_section(news_dir, limit=3)

    lines = [line for line in section.splitlines() if line.startswith("- ")]
    assert len(lines) == 3
    assert "2026-05-10" in lines[0]


def test_render_latest_section_uses_relative_paths(tmp_path: Path) -> None:
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    (news_dir / "2026-05-17.md").write_text("# x\n")

    section = render_latest_section(news_dir, limit=30)

    assert "news/2026-05-17.md" in section


def test_update_readme_replaces_marker_block(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "# kamo-news\n\n"
        "## 最新記事\n\n"
        "<!-- LATEST:START -->\n"
        "古い内容\n"
        "<!-- LATEST:END -->\n\n"
        "## アーカイブ\n"
    )
    news_dir = tmp_path / "news"
    news_dir.mkdir()
    (news_dir / "2026-05-17.md").write_text("# AI トレンドニュース 2026-05-17\n")

    update_readme(readme, news_dir, limit=30)

    content = readme.read_text()
    assert "古い内容" not in content
    assert "2026-05-17" in content
    assert "<!-- LATEST:START -->" in content
    assert "<!-- LATEST:END -->" in content
    assert "## アーカイブ" in content  # 後続セクションが破壊されない


def test_update_readme_errors_if_markers_missing(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# kamo-news\n\n本文のみ\n")
    news_dir = tmp_path / "news"
    news_dir.mkdir()

    with pytest.raises(ValueError, match="markers"):
        update_readme(readme, news_dir, limit=30)
