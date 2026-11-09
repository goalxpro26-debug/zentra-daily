# Zentra Daily

World news, sports, entertainment, AI & learning, clearly explained.

Astro static site, launch-ready for Cloudflare Pages (owner deploys Cloudflare himself — see `LAUNCH.md`).

## Design

Follows the Dribbble shot "News Website | boxing" by Valtorian (VERTONEWS): monochrome, centred white card, hero + sidebar layout, rounded corners, colour only from imagery.

## Content

8 launch articles (600+ words each), all real news from November 8–9, 2026, each with a named credible source and a Sources section. No invented quotes or facts. Images are clearly labelled illustrations — never presented as real event photographs.

## Develop

```
npm install
npm run dev
npm run build   # runs the sitemap generator, then astro build
```
