import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";

export async function GET(context: APIContext) {
  const entries = (await getCollection("news")).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime(),
  );

  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const siteOrigin = (context.site ?? new URL("https://kamo-shika.github.io")).origin;
  const channelLink = `${siteOrigin}${base}/`;

  return rss({
    title: "kamo-news",
    description:
      "Claude Code が毎朝 7:00 JST に自動生成する AI トレンドニュース。LLM・生成 AI・エージェントの動向を日次でまとめて配信。",
    site: channelLink,
    items: entries.map((entry) => ({
      title: entry.data.title,
      description: entry.data.description,
      pubDate: entry.data.date,
      link: `${base}/${entry.id.replace(/\.md$/, "")}/`,
      categories: entry.data.tags,
    })),
    customData: "<language>ja-jp</language>",
    trailingSlash: true,
  });
}
