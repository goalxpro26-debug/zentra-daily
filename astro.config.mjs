import { defineConfig } from 'astro/config';

// Static output — deploy the dist/ folder to Cloudflare Pages.
// No server adapter needed, so hosting stays free and fast.
export default defineConfig({
  output: 'static',
});
