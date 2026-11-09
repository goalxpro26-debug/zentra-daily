# Launch Zentra Daily yourself — Cloudflare Pages

Muse does NOT deploy this — you do, in Cloudflare. Everything else is ready.

## What is ready

- Astro static site: homepage (Dribbble VERTONEWS design), 8 real articles with named sources, 12 category pages, About page, custom 404
- SEO: sitemap generated on every build, robots.txt, Open Graph tags
- Repo: https://github.com/goalxpro26-debug/zentra-daily

## Deploy in Cloudflare Pages (5 minutes)

1. Cloudflare Dashboard → Pages → Create application → Pages → Connect to Git
2. Select repo: `goalxpro26-debug/zentra-daily`, branch: `main`
3. Framework preset: Astro (or leave blank and set manually below)
4. Build command: `npm run build`
5. Build output directory: `dist`
6. Save and Deploy — first deploy takes a couple of minutes

Every future push to `main` redeploys automatically. No Wrangler login needed for this path.

## After your first deploy (optional, recommended)

1. Note your `*.pages.dev` URL from Cloudflare.
2. If you want the sitemap to use that exact URL, rebuild once with:
   ```
   SITE_URL=https://YOUR-SITE.pages.dev npm run build
   ```
   Then push — the sitemap regenerates. The site works fine without this step.
3. Optional custom domain: Pages → Custom domains → Set up a custom domain, then follow Cloudflare's DNS instructions for your domain (for example zentradaily.com — check availability and trademark first; not yet verified).

## Adding a new article

1. Add a Markdown file in `src/content/articles/` with the same frontmatter as the existing ones (title, excerpt, category, categorySlug, date, author, heroLabel, heroTone, sourceName, sourceUrl).
2. Write 600+ words from a named credible source, link it in the Sources section, and label any image "Illustration" — never present an illustration as a real event photo.
3. Run `npm run build` to check it, then push to `main` — Cloudflare redeploys automatically.

## If a build fails

- Check the Cloudflare build log for the failing step first.
- Local check that must pass before re-deploying:
  ```
  npm install
  npm run build
  ```
- Never hand-edit `public/sitemap.xml` — it is generated from the articles on every build.
