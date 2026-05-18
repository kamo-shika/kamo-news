# 出力フォーマット

`news/YYYY-MM-DD.md` のテンプレート。すべての記事はこの構造に従う。

## テンプレート

```markdown
---
title: "AI トレンドニュース YYYY-MM-DD"
date: YYYY-MM-DD
description: "<RSS / OGP 用の 1〜2 文サマリ。80〜120 文字>"
tags: [<記事内カテゴリの集合体。例: "論文", "ツール", "議論">]
---

# AI トレンドニュース YYYY-MM-DD

> 自動生成 (Claude Code on GitHub Actions)

## 今日のハイライト

- <1 行サマリ 1>
- <1 行サマリ 2>
- <1 行サマリ 3>

## トピック

### 1. <タイトル>

<3〜5 文の要約。日本語。>

- 出典: <URL>
- カテゴリ: <論文 | 公式リリース | 議論 | ツール | その他>

### 2. <タイトル>

...

---

## 情報源サマリ

- Hugging Face Daily Papers: N 件取得
- arXiv cs.CL/cs.AI: N 件取得
- Hacker News: N 件取得
- はてブ AI タグ: N 件取得
- 公式ブログ (Anthropic/OpenAI/DeepMind/HF): N 件取得

取得失敗: <ソース名> (理由)
```

## フロントマター仕様

YAML フロントマター (`---` で囲む) を **ファイル先頭に必ず配置**する。Astro の Content Collection / RSS フィードが参照する。

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `title` | string | 必須 | H1 と同じ文字列。クォートで囲む。 |
| `date` | string | 必須 | `YYYY-MM-DD` 形式。クォートなし (Astro が Date として解釈する)。 |
| `description` | string | 必須 | RSS の `<description>` および OGP description。「今日のハイライト」を 1〜2 文に圧縮、80〜120 文字目安。 |
| `tags` | array | 必須 | 当日の各トピックの `カテゴリ:` 値をユニーク化したもの。例: `["論文", "ツール", "議論"]` |

`description` の生成ルール:
- ハイライトの主要 2〜3 トピックを「、」で並べて文末に「など」を付ける形が基本
- 例: `"Darwin Family、WildClawBench、Apple Silicon コスト実測など"`

## 規約

- タイトル: H1 は記事全体のタイトル、H2 はセクション (`今日のハイライト`、`トピック`、`情報源サマリ`)、H3 は各トピック
- ハイライトは記事を読まなくても要点が掴める 1 行
- トピック番号は重要度順 (1 が最重要)
- 出典 URL は必ず 1 つ以上、複数ある場合は要約直後に箇条書きで列挙
- 出典 URL は markdownlint の MD034 (bare URLs) を避けるため、必ず `<https://example.com/path>` のように山括弧で囲む。`[テキスト](https://...)` 形式も可。bare な `https://...` を本文中にそのまま書かない
- カテゴリは規定の 5 種類から選ぶ
- 日付フォーマットは `YYYY-MM-DD` で統一
