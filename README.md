# kamo-news

毎朝 7:00 JST に Claude Code が自動生成する AI トレンドニュース。

## 仕組み

GitHub Actions が日次で起動し、Claude Code Action が `.claude/skills/ai-trend-daily/` スキルに従って情報収集・記事生成・セルフレビューを行い、PR を作成します。検証を通過した PR は自動マージされ、`news/` ディレクトリに記事が蓄積されます。

## 最新記事

<!-- LATEST:START -->
<!-- LATEST:END -->

## アーカイブ

[news/](news/) ディレクトリを参照。
