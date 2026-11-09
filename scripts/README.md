# Zentra Daily — RSS draft pipeline

## The pattern learned from the videos (researched, not watched)

The YouTube list the owner pasted is a search dump about scraping and
automating news. The methods were researched from video descriptions,
transcripts and the matching n8n workflow templates — the videos
themselves were not watched, and nothing below claims otherwise.

**Common pattern across them (5–8 points):**

1. **RSS is the input, not page scraping.** Jake Dawson's news flow starts
   from Inoreader RSS, Duncan Rogoff's viral-news agent and his daily
   digest both start from RSS feeds, and the n8n news-to-blog template
   starts from Google News headlines. RSS gives titles, links and short
   summaries with no JavaScript, no key and no browser.
2. **A schedule trigger paces it.** Rogoff's workflows run on a schedule
   trigger (hourly/daily); the n8n RSS-curator template recommends every
   6–12 hours; the Hack'celeration tech-blog workflow fires once a day at
   8:00 AM. Polling is a long-running habit, not a one-shot scrape.
3. **Filter before you write.** Rogoff filters by recency (last 24 hours)
   and by keyword/relevance; Matt Carter filters Google Trends to the
   niche, then looks up only the matching Google News results; the n8n
   RSS curator scores articles and keeps only priority ≥ 60.
4. **AI turns raw items into structure, not into a finished post.**
   Carter's flow feeds scraped news into an AI that returns *bullet-point
   content ideas*; Rogoff's digest AI summarises and rewrites in plain
   English; the n8n curator AI writes a summary + category + priority.
   The AI's job is triage and outlining — the human (or a separate,
   reviewed step) decides what ships.
5. **Output lands in a queue, not straight on the site.** Dawson logs to
   Google Sheets, Carter/Rogoff use Airtable/Notion, the n8n news-to-blog
   template logs to Google Sheets. There is always a holding store between
   discovery and publishing.
6. **De-duplicate by URL/title.** The Google News RSS guides and the n8n
   news-to-blog template both de-duplicate by resolved URL (or normalised
   title + source) so the same story is counted once across polls.
7. **Then comes the part Zentra Daily does NOT copy: auto-publish.**
   Yves Lummer's "100% Automated" WordPress site, the Boxput free AI news
   script, the n8n news-to-blog template and the Blogger auto-blogging
   guides all end with AI writing the full article and publishing it
   straight to WordPress/Blogger for AdSense. That is exactly what the
   owner's blueprint forbids.
8. **The heavy-scraping variants are also not copied.** Tech With Tim's
   scraping agent drives a real browser and uses paid data APIs (Bright
   Data / SerpAPI); Matt Carter's full flow scrapes *full article
   content* via Firecrawl. Zentra Daily uses public RSS only — no
   browser automation, no paid scraping APIs, no CAPTCHA/bot-evasion, no
   pretending to be Googlebot.

## How this pipeline maps to the pattern

```
RSS feeds (Google News topics/search, BBC, The Verge)
        │  fetch-drafts.py — stdlib only, cron-able
        ▼
Draft queue — src/content/drafts/  (Markdown outlines, NOT articles)
        │  human editor picks 2–4/day, verifies, rewrites fresh
        ▼
Finished article — src/content/articles/  (600+ words, Sources section)
        │  npm run build
        ▼
Cloudflare Pages deploy (owner deploys)
```

## What it deliberately does NOT do

- **No full-text scraping.** It never fetches a publisher's article page
  for body text. The only URL it resolves is a Google News redirect, to
  learn the publisher's canonical link for the Sources section.
- **No auto-publish.** Drafts live in `src/content/drafts/`, which is not
  an Astro content collection — `npm run build` never puts them on the
  site. The human editor is the sole publisher.
- **No verbatim copying.** Drafts contain the RSS headline + a short RSS
  summary (truncated, labelled as such) + an outline + "to verify"
  notes. Articles are written fresh, in Zentra Daily's own words.
- **No paywall bypass / bot evasion.** Public RSS only, one polite fetch
  per feed per run, identifying User-Agent, 15 s timeout.

## Feeds

Per category, in priority order (first feed that yields fresh items wins
the category's slots):

| Category | Feeds |
|---|---|
| World | Google News WORLD, BBC World |
| Politics | Google News NATION, BBC Politics |
| Business & Economy | Google News BUSINESS, BBC Business |
| Technology & AI | Google News TECHNOLOGY, BBC Technology, The Verge |
| Science & Environment | Google News SCIENCE, BBC Science & Environment |
| Society | Google News search "society" |
| Entertainment | Google News ENTERTAINMENT, BBC Entertainment & Arts |
| Sports | Google News SPORTS, BBC Sport |
| Students | Google News search "students" |
| Learning | Google News search "education learning" |
| Health | Google News HEALTH, BBC Health |
| Culture | Google News search "culture arts" |

Reuters and AP direct RSS were tested 2026-11-08 and are blocked from
this environment (Reuters 401, AP 403), so they are not in the feed list.
Their stories still reach the queue through Google News, which aggregates
both. If their RSS becomes reachable, add them to `FEEDS` in
`fetch-drafts.py`.

## Running it

```bash
python3 scripts/fetch-drafts.py            # fetch + write new drafts
python3 scripts/fetch-drafts.py --dry-run  # show what would be queued
```

Suggested schedule (see the daily plan in the parent report): run once in
the morning (~08:00) and once in the evening (~18:00). Reruns are safe —
`scripts/seen.json` remembers queued stories, and drafts are capped at
3 per category / 15 total per run.

## Files

- `fetch-drafts.py` — the pipeline (Python stdlib only).
- `seen.json` — seen-story keys (URLs + titles), created on first run.
- `../src/content/drafts/` — the draft queue (never published by the build).
