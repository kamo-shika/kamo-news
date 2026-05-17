# kamo-news

毎朝 7:00 JST に Claude Code が自動生成する AI トレンドニュース。

## 仕組み

GitHub Actions が日次で起動し、Claude Code Action が `.claude/skills/ai-trend-daily/` スキルに従って情報収集・記事生成・セルフレビューを行い、PR を作成します。検証を通過した PR は自動マージされ、`news/` ディレクトリに記事が蓄積されます。

## 最新記事

<!-- LATEST:START -->
- [AI トレンドニュース 2026-05-17](news/2026-05-17.md)
<!-- LATEST:END -->

## アーカイブ

[news/](news/) ディレクトリを参照。

## 運用

### 手動実行

```bash
gh workflow run daily-news.yml
gh workflow run daily-news.yml -f target_date=2026-05-17  # 日付指定
```

### OAuth トークン更新

サブスクの OAuth トークンは最大 1 年有効。失効したら:

```bash
claude setup-token
gh secret set CLAUDE_CODE_OAUTH_TOKEN
```

### セルフレビュー Fail 時

draft PR に `needs-review` ラベルが付く。本文を確認して:

- 内容が許容範囲 → ラベル外して draft 解除 → auto-merge が走る
- 内容が NG → PR を close、`gh workflow run daily-news.yml -f target_date=<日付>` で再生成
