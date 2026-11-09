import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    category: z.string(),
    categorySlug: z.string(),
    date: z.string(),
    author: z.string(),
    heroLabel: z.string(),
    heroTone: z.string(),
    sourceName: z.string(),
    sourceUrl: z.string(),
    sourceName2: z.string().optional(),
    sourceUrl2: z.string().optional(),
  }),
});

export const collections = { articles };
