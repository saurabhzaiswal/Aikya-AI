export const SOCIAL_IMAGES = {
  product: {
    path: '/og/aikya-product.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Understand what matters, in your language, beside converging multilingual document paths.',
  },
  features: {
    path: '/og/aikya-features.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Translation that respects the work around the words, beside converging document paths.',
  },
  pricing: {
    path: '/og/aikya-pricing.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Start focused, grow with understanding, beside converging document paths.',
  },
  knowledge: {
    path: '/og/aikya-knowledge.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Knowledge should travel without losing meaning, beside connected notes and an open guide.',
  },
  trust: {
    path: '/og/aikya-trust.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Privacy is part of understanding, beside paper ribbons sheltering a document.',
  },
  about: {
    path: '/og/aikya-about.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Built from one belief, understanding should be shared, beside a protected document.',
  },
  blog: {
    path: '/og/aikya-blog.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: Notes from building a calmer language product, beside woven multilingual reading bands.',
  },
  blogFoundation: {
    path: '/og/aikya-blog-foundation.jpg',
    width: 1200,
    height: 630,
    type: 'image/jpeg',
    alt: 'Aikya message: The foundation before the feature rush, beside a protected modular reading system.',
  },
} as const

export type SocialImageKey = keyof typeof SOCIAL_IMAGES

const CONTENT_SOCIAL_IMAGES: Readonly<Record<string, SocialImageKey>> = {
  '/blog/phase-1-foundation': 'blogFoundation',
}

export function resolveContentSocialImage(path: string, fallback: SocialImageKey): SocialImageKey {
  return CONTENT_SOCIAL_IMAGES[path] ?? fallback
}
