// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

const repo = process.env.GITHUB_REPOSITORY ?? "kamo-shika/kamo-news";
const repoName = repo.split("/")[1];
const owner = repo.split("/")[0];

const isProd = process.env.NODE_ENV === "production" || process.env.CI === "true";

export default defineConfig({
  site: isProd ? `https://${owner}.github.io` : "http://localhost:4321",
  base: isProd ? `/${repoName}` : "/",
  trailingSlash: "always",
  output: "static",
  integrations: [sitemap()],
});
