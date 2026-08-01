import { FOUNDER, SITE_NAME } from './constants'

export function organizationSchema(siteUrl: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': SITE_NAME,
    'url': siteUrl,
    'founder': { '@type': 'Person', 'name': FOUNDER.name, 'url': FOUNDER.portfolio },
    'sameAs': [FOUNDER.linkedIn, FOUNDER.github, FOUNDER.dev],
  }
}

export function softwareSchema(siteUrl: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    'name': SITE_NAME,
    'applicationCategory': 'BusinessApplication',
    'operatingSystem': 'Web',
    'url': siteUrl,
    'description': 'Privacy-focused text and digital PDF translation workspace.',
  }
}

export function breadcrumbSchema(siteUrl: string, items: Array<{ name: string, path: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': items.map((item, index) => ({
      '@type': 'ListItem',
      'position': index + 1,
      'name': item.name,
      'item': new URL(item.path, siteUrl).toString(),
    })),
  }
}

export function faqSchema(items: Array<{ question: string, answer: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    'mainEntity': items.map(item => ({
      '@type': 'Question',
      'name': item.question,
      'acceptedAnswer': { '@type': 'Answer', 'text': item.answer },
    })),
  }
}
