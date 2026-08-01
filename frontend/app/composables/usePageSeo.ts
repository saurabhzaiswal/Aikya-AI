import { SITE_NAME } from '~/seo/constants'
import type { PageMetadata } from '~/seo/metadata'

interface SeoOptions extends PageMetadata {
  path?: string
  noIndex?: boolean
  schemas?: Array<Record<string, unknown>>
}

export function usePageSeo(options: SeoOptions): void {
  const canonical = useCanonical(options.path)
  const title = `${options.title} · ${SITE_NAME}`
  useSeoMeta({
    title,
    description: options.description,
    ogTitle: title,
    ogDescription: options.description,
    ogType: 'website',
    ogUrl: canonical,
    ogSiteName: SITE_NAME,
    twitterCard: 'summary_large_image',
    robots: options.noIndex ? 'noindex, nofollow' : 'index, follow',
  })
  if (options.schemas?.length) useSchema(options.schemas)
}
