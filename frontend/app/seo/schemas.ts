import { DEFAULT_DESCRIPTION, FOUNDER, SITE_NAME } from './constants'

function canonicalSiteUrl(siteUrl: string): string {
  return new URL('/', siteUrl).toString()
}

export function organizationSchema(siteUrl: string) {
  const url = canonicalSiteUrl(siteUrl)
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': `${url}#organization`,
    'name': SITE_NAME,
    'alternateName': 'Aikya',
    'url': url,
    'logo': {
      '@type': 'ImageObject',
      'url': new URL('/brand/aikya-app-icon-512.png', url).toString(),
      'contentUrl': new URL('/brand/aikya-app-icon-512.png', url).toString(),
      'caption': SITE_NAME,
    },
    'description': DEFAULT_DESCRIPTION,
    'founder': { '@type': 'Person', 'name': FOUNDER.name, 'url': FOUNDER.portfolio },
    'sameAs': [FOUNDER.linkedIn, FOUNDER.github, FOUNDER.dev],
  }
}

export function websiteSchema(siteUrl: string) {
  const url = canonicalSiteUrl(siteUrl)
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${url}#website`,
    'url': url,
    'name': SITE_NAME,
    'alternateName': 'Aikya',
    'description': DEFAULT_DESCRIPTION,
    'inLanguage': 'en',
    'publisher': { '@id': `${url}#organization` },
  }
}

export function softwareSchema(siteUrl: string) {
  const url = canonicalSiteUrl(siteUrl)
  return {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    'name': SITE_NAME,
    'applicationCategory': 'BusinessApplication',
    'operatingSystem': 'Web',
    'url': url,
    'description': DEFAULT_DESCRIPTION,
    'image': new URL('/og/aikya-product.jpg', url).toString(),
    'publisher': { '@id': `${url}#organization` },
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
