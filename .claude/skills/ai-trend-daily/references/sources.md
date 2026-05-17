# 情報源リスト

すべて認証不要・公開 API/RSS。取得失敗時はそのソースをスキップして次へ進む。

## 論文

### Hugging Face Daily Papers

- URL: `https://huggingface.co/api/daily_papers`
- 取得: `curl -s 'https://huggingface.co/api/daily_papers'`
- 形式: JSON (配列)
- フィルタ: 当日 (UTC) の `publishedAt` を持つもの
- 抽出: `.[] | {title, url: ("https://huggingface.co/papers/" + .paper.id), summary: .paper.summary}`

### arXiv cs.CL / cs.AI

- URL: `http://export.arxiv.org/api/query?search_query=cat:cs.CL+OR+cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=20`
- 取得: `curl -s '...'`
- 形式: Atom XML
- フィルタ: 過去 24 時間以内の `published`
- 注意: 学術論文なので AI 関連性は cs.CL / cs.AI で十分絞れている

## コミュニティ

### Hacker News

- 一覧 URL: `https://hacker-news.firebaseio.com/v0/topstories.json`
- アイテム URL: `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- 取得手順:
  1. topstories で ID 配列を取得
  2. 上位 30 件のアイテムを並列取得
  3. title に "AI", "LLM", "GPT", "Claude", "Gemini", "Llama", "model", "agent" 等を含むものをフィルタ

### はてなブックマーク (AI タグ)

- URL: `https://b.hatena.ne.jp/q/AI?target=tag&users=10&safe=on&mode=rss`
- 取得: `curl -s 'https://b.hatena.ne.jp/q/AI?target=tag&users=10&safe=on&mode=rss'`
- 形式: RSS 2.0
- フィルタ: 過去 24 時間以内の `pubDate`、ブックマーク数 10 以上

## 公式ブログ (RSS)

### Anthropic

- URL: `https://www.anthropic.com/news/rss.xml`
- 形式: RSS

### OpenAI

- URL: `https://openai.com/blog/rss.xml`
- 形式: RSS

### Google DeepMind

- URL: `https://deepmind.google/blog/rss.xml`
- 形式: RSS

### Hugging Face

- URL: `https://huggingface.co/blog/feed.xml`
- 形式: Atom

## エラー処理

- いずれかの情報源が 4xx/5xx を返した、またはタイムアウトした場合: そのソースをスキップしてログに記録 (記事には含めない)
- すべての情報源が死んでいた場合: 記事を生成せず、ジョブを失敗させる
