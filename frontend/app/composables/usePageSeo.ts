import { SITE_NAME } from '~/seo/constants'
import type { PageMetadata } from '~/seo/metadata'
import { SOCIAL_IMAGES } from '~/seo/social-images'

interface SeoOptions extends PageMetadata {
  path?: string
  noIndex?: boolean
  schemas?: Array<Record<string, unknown>>
}

export function usePageSeo(options: SeoOptions): void {
  const canonical = useCanonical(options.path)
  const config = useRuntimeConfig()
  const title = `${options.title} · ${SITE_NAME}`
  const socialImage = SOCIAL_IMAGES[options.socialImage ?? 'product']
  const socialImageUrl = new URL(socialImage.path, config.public.siteUrl).toString()
  const secureSocialImageUrl = socialImageUrl.startsWith('https://') ? socialImageUrl : undefined
  useSeoMeta({
    title,
    description: options.description,
    ogTitle: title,
    ogDescription: options.description,
    ogType: 'website',
    ogUrl: canonical,
    ogSiteName: SITE_NAME,
    ogLocale: 'en_US',
    ogImage: socialImageUrl,
    ogImageSecureUrl: secureSocialImageUrl,
    ogImageType: socialImage.type,
    ogImageWidth: socialImage.width,
    ogImageHeight: socialImage.height,
    ogImageAlt: socialImage.alt,
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: options.description,
    twitterImage: socialImageUrl,
    twitterImageAlt: socialImage.alt,
    robots: options.noIndex
      ? 'noindex, nofollow'
      : 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
  })
  if (options.schemas?.length) useSchema(options.schemas)
}
