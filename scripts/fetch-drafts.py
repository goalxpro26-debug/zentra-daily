#!/usr/bin/env python3
"""Zentra Daily — RSS draft pipeline (discovery only, NEVER auto-publish).

What this does
---------------
1. Fetches PUBLIC RSS feeds (Google News topics/search + BBC + The Verge)
   — headlines, short summaries and links only.
2. Filters to the last 24 hours, de-duplicates by URL/title, and keeps at
   most 3 stories per category (12-15 total), balanced across categories.
3. Writes one Markdown DRAFT per story into
   ``src/content/drafts/`` — an outline + key facts taken from the RSS
   summary + "to verify" notes. NOT a finished article, NOT copied text.
4. Remembers seen stories in ``scripts/seen.json`` so reruns do not
   re-queue the same story.

What this deliberately does NOT do
-----------------------------------
- No full-article scraping. The script never fetches a publisher's article
  page for its body text. Google News links do not HTTP-redirect to the
  publisher (the publisher URL is encoded inside the link token), so the
  script keeps the working Google News story link and names the publisher
  from the title suffix instead.
- No auto-publish. Drafts live in ``src/content/drafts/``, which is NOT an
  Astro content collection, so ``npm run build`` never puts them on the
  site. A human editor (the owner / Muse with review) picks 2-4 drafts a
  day, verifies the facts against the named source, writes the article
  fresh in Zentra Daily's own words, and only then moves it to
  ``src/content/articles/``.
- No paywall bypassing, no bot-evasion, no fake user-agents, no pretending
  to be Googlebot. Feeds are fetched once per run with a polite
  identifying User-Agent and a 15s timeout.

Usage
-----
    python3 scripts/fetch-drafts.py            # fetch + write new drafts
    python3 scripts/fetch-drafts.py --dry-run  # show what would be queued
    python3 scripts/fetch-drafts.py --max-total 15 --max-per-category 3

Then: pick drafts, verify, write the article, move it to articles/.

Stdlib only — no feedparser, no extra dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "src" / "content" / "drafts"
SEEN_PATH = Path(__file__).resolve().parent / "seen.json"

USER_AGENT = "ZentraDaily/1.0 (RSS draft discovery; +https://github.com/goalxpro26-debug/zentra-daily)"
FETCH_TIMEOUT = 15
MAX_AGE = timedelta(hours=24)

GN = "https://news.google.com/rss/headlines/section/topic/{topic}?hl=en-US&gl=US&ceid=US:EN"
GN_SEARCH = "https://news.google.com/rss/search?q={q}%20when:1d&hl=en-US&gl=US&ceid=US:EN"
BBC = "https://feeds.bbci.co.uk/news/{feed}/rss.xml"

# (category name, category slug, [feed urls])
FEEDS: list[tuple[str, str, list[str]]] = [
    ("World", "world", [
        GN.format(topic="WORLD"),
        BBC.format(feed="world"),
    ]),
    ("Politics", "politics", [
        GN.format(topic="NATION"),
        BBC.format(feed="politics"),
    ]),
    ("Business & Economy", "business-economy", [
        GN.format(topic="BUSINESS"),
        BBC.format(feed="business"),
    ]),
    ("Technology & AI", "technology-ai", [
        GN.format(topic="TECHNOLOGY"),
        BBC.format(feed="technology"),
        "https://www.theverge.com/rss/index.xml",
    ]),
    ("Science & Environment", "science-environment", [
        GN.format(topic="SCIENCE"),
        BBC.format(feed="science_and_environment"),
    ]),
    ("Society", "society", [
        GN_SEARCH.format(q="society"),
    ]),
    ("Entertainment", "entertainment", [
        GN.format(topic="ENTERTAINMENT"),
        BBC.format(feed="entertainment_and_arts"),
    ]),
    ("Sports", "sports", [
        GN.format(topic="SPORTS"),
        BBC.format(feed="sport"),
    ]),
    ("Students", "students", [
        GN_SEARCH.format(q="students"),
    ]),
    ("Learning", "learning", [
        GN_SEARCH.format(q="education+learning"),
    ]),
    ("Health", "health", [
        GN.format(topic="HEALTH"),
        BBC.format(feed="health"),
    ]),
    ("Culture", "culture", [
        GN_SEARCH.format(q="culture+arts"),
    ]),
]


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.read()


def resolve_url(url: str) -> str:
    """Follow redirects to the publisher's canonical link.

    Google News RSS links are news.google.com/rss/articles/... redirects.
    We open the URL (no body read) purely to learn the final address for
    the Sources section. If resolving fails, keep the original link.
    """
    if "news.google.com/rss/articles" not in url:
        return url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT},
                                     method="HEAD")
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            return resp.geturl()
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
                return resp.geturl()
        except Exception:
            return url


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_pubdate(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw.strip())
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:70].strip("-") or "story"


def publisher_from_title(title: str) -> str | None:
    """Google News RSS titles carry the publisher after the last ' - '.

    The Google News link itself does not HTTP-redirect to the publisher
    (the publisher URL is encoded inside the CBMi token), so the honest
    source name comes from the title suffix, e.g. '... - The Guardian'.
    """
    if " - " not in title:
        return None
    suffix = title.rsplit(" - ", 1)[1].strip()
    if 2 < len(suffix) <= 40 and not any(c in suffix for c in ".!?"):
        return suffix
    return None


def source_name_from_url(url: str) -> str:
    host = urllib.request.urlparse(url).netloc
    host = re.sub(r"^www\.", "", host)
    return host


def parse_feed(xml: bytes, category: str, slug: str) -> list[dict]:
    items: list[dict] = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return items
    for item in root.iter("item"):
        title = strip_html(item.findtext("title") or "")
        link = (item.findtext("link") or "").strip()
        summary = strip_html(item.findtext("description") or "")
        pub = parse_pubdate(item.findtext("pubDate") or "")
        if not title or not link:
            continue
        items.append({
            "title": title,
            "link": link,
            "summary": summary,
            "published": pub,
            "category": category,
            "categorySlug": slug,
        })
    return items


def load_seen() -> dict:
    if SEEN_PATH.exists():
        try:
            return json.loads(SEEN_PATH.read_text())
        except json.JSONDecodeError:
            return {"urls": [], "titles": []}
    return {"urls": [], "titles": []}


def save_seen(seen: dict) -> None:
    SEEN_PATH.write_text(json.dumps(seen, indent=2, sort_keys=True) + "\n")


def story_key(item: dict) -> str:
    return hashlib.sha256(
        (item["link"].lower().rstrip("/") + "|" + item["title"].lower()).encode()
    ).hexdigest()[:16]


def draft_filename(item: dict) -> str:
    date = (item["published"] or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    return f"{date}-{slugify(item['title'])}.md"


def write_draft(item: dict) -> Path:
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    path = DRAFTS_DIR / draft_filename(item)
    # Avoid clobbering an existing draft for the same story.
    if path.exists():
        stem, i = path.stem, 2
        while (DRAFTS_DIR / f"{stem}-{i}.md").exists():
            i += 1
        path = DRAFTS_DIR / f"{stem}-{i}.md"

    summary = item["summary"]
    if len(summary) > 600:
        summary = summary[:600].rstrip() + " …"

    body = f"""---
title: "{item['title'].replace('"', "'")}"
sourceName: "{item['source_name']}"
sourceUrl: "{item['link']}"
category: "{item['category']}"
categorySlug: "{item['categorySlug']}"
published: "{(item['published'] or datetime.now(timezone.utc)).isoformat()}"
fetched: "{datetime.now(timezone.utc).isoformat()}"
status: draft
---

# DRAFT — DO NOT PUBLISH AS-IS

This file is a **discovery draft only**. It is not an article: it must be
verified against the source, rewritten fresh in Zentra Daily's own words,
and moved to `src/content/articles/` by a human editor before it can go
live. Drafts in this folder are never built into the site.

## Story

**Source:** [{item['source_name']}]
({item['link']})

**Published:** {(item['published'] or 'unknown')}

## RSS summary (headline + short summary only — NOT article text)

{summary or '(No summary in the feed.)'}

## Outline (to fill in while writing)

- Lead: who / what / where / when, in one sentence.
- What happened: the key facts, each verified against the source.
- Why it matters: context for a general reader.
- What is still unknown / disputed: say so explicitly; do not fill gaps.

## To verify before writing

- [ ] Open the source link and confirm the facts above are still current.
- [ ] Confirm names, numbers and dates against the source (and a second
      credible source for anything contested).
- [ ] Do not copy the source headline or wording — write a fresh headline.
- [ ] Add a Sources section linking the source(s) used.
- [ ] 600+ words, Zentra Daily style (clear, plain, no hype).
"""
    path.write_text(body)
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Zentra Daily RSS draft pipeline")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would be queued, write nothing")
    ap.add_argument("--max-per-category", type=int, default=3)
    ap.add_argument("--max-total", type=int, default=15)
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    cutoff = now - MAX_AGE
    seen = load_seen()
    seen_urls = set(seen.get("urls", []))
    seen_titles = set(seen.get("titles", []))

    per_category: dict[str, list[dict]] = {}
    feed_errors: list[str] = []
    fetched = 0

    for category, slug, urls in FEEDS:
        picked: list[dict] = []
        for feed_url in urls:
            try:
                xml = fetch_bytes(feed_url)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                feed_errors.append(f"{feed_url} — {exc}")
                continue
            for item in parse_feed(xml, category, slug):
                fetched += 1
                if item["published"] and item["published"] < cutoff:
                    continue
                if not item["published"]:
                    continue  # no date = cannot prove it is from the last 24h
                key = story_key(item)
                if key in seen_urls or item["title"].lower() in seen_titles:
                    continue
                if any(story_key(p) == key for p in picked):
                    continue
                if any(p["title"].lower() == item["title"].lower() for p in picked):
                    continue
                picked.append(item)
                if len(picked) >= args.max_per_category:
                    break
            if len(picked) >= args.max_per_category:
                break
        per_category[category] = picked

    # Balance: take round-robin across categories so no category hogs the queue.
    queue: list[dict] = []
    for i in range(args.max_per_category):
        for category, _, _ in FEEDS:
            if len(queue) >= args.max_total:
                break
            items = per_category.get(category, [])
            if i < len(items):
                queue.append(items[i])
        if len(queue) >= args.max_total:
            break

    print(f"Fetched {fetched} feed items; {sum(len(v) for v in per_category.values())} "
          f"fresh, unseen stories in the last 24h.")
    for category, _, _ in FEEDS:
        n = len(per_category.get(category, []))
        print(f"  {category}: {n}")
    if feed_errors:
        print("Feed errors (skipped, not fatal):")
        for err in feed_errors:
            print(f"  - {err}")

    if args.dry_run:
        print(f"\nDRY RUN — would queue {len(queue)} drafts, wrote nothing.")
        for item in queue:
            print(f"  [{item['category']}] {item['title']}")
        return 0

    written: list[Path] = []
    for item in queue:
        item["link"] = resolve_url(item["link"])
        if "news.google.com" in item["link"]:
            # The Google News link does not HTTP-redirect to the publisher;
            # it is a working story page in its own right. Name the
            # publisher from the title suffix instead.
            item["source_name"] = publisher_from_title(item["title"]) or "Google News"
        else:
            item["source_name"] = source_name_from_url(item["link"])
        written.append(write_draft(item))
        seen_urls.add(story_key(item))
        seen_titles.add(item["title"].lower())

    seen["urls"] = sorted(seen_urls)
    seen["titles"] = sorted(seen_titles)
    save_seen(seen)

    print(f"\nWrote {len(written)} draft(s) to {DRAFTS_DIR}:")
    for path in written:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
