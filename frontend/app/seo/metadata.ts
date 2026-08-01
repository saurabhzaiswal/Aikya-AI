import { DEFAULT_DESCRIPTION } from './constants'

export interface PageMetadata {
  title: string
  description: string
}

export const PAGE_METADATA = {
  home: {
    title: 'Private document and text translation',
    description: DEFAULT_DESCRIPTION,
  },
  features: {
    title: 'Text and digital PDF translation features',
    description: 'Explore the focused Aikya AI Phase 1 workspace for text translation and readable digital PDF translation.',
  },
  pricing: {
    title: 'Pricing',
    description: 'Aikya AI is in its private MVP phase. Learn how early access and future pricing will be handled.',
  },
  about: {
    title: 'About Aikya AI',
    description: 'Learn why solo founder Saurabh Choudhary is building Aikya AI to reduce language barriers.',
  },
  contact: {
    title: 'Contact',
    description: 'Connect with Aikya AI founder Saurabh Choudhary through verified public profiles.',
  },
  privacy: {
    title: 'Privacy policy draft',
    description: 'Read the current draft privacy notice for the Aikya AI Phase 1 MVP.',
  },
  terms: {
    title: 'Terms of service draft',
    description: 'Read the current draft terms for the Aikya AI Phase 1 MVP.',
  },
} satisfies Record<string, PageMetadata>
