import { readdirSync } from 'node:fs';
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const base = (process.env.SITE_URL || 'https://zentra-daily.pages.dev').replace(/\/$/, '');
const esc = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

const articleSlugs = readdirSync(join(root, 'src/content/articles'))
  .filter((f) => f.endsWith('.md'))
  .map((f) => f.replace(/\.md$/, ''));

const categorySlugs = ['world', 'politics', 'business-economy', 'technology-ai', 'science-environment', 'society', 'entertainment', 'sports', 'students', 'learning', 'health', 'culture'];

const urls = [
  '',
  '/about/',
  ...articleSlugs.map((s) => `/articles/${s}/`),
  ...categorySlugs.map((s) => `/category/${s}/`),
];

const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${esc(base + u)}</loc></url>`).join('\n')}\n</urlset>\n`;
writeFileSync(join(root, 'public/sitemap.xml'), xml);
console.log(`Built sitemap: ${urls.length} URLs → public/sitemap.xml (base: ${base})`);
