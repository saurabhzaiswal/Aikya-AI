# SEO, Brand Assets, and Social Sharing

Status: Phase 1 implementation baseline  
Last updated: 2026-08-02

## Purpose

Aikya's public Nuxt routes expose consistent identity and complete crawlable sharing metadata without adding runtime image generation, browser listeners, analytics, or a new frontend dependency. Authentication and `/app/**` routes remain `noindex`, excluded from the sitemap, and outside the public sharing surface. Because those routes are client-rendered, Nitro also returns an explicit `X-Robots-Tag: noindex, nofollow` header rather than relying only on a hydrated meta tag.

## Brand assets

| Asset | Purpose |
|---|---|
| `frontend/public/brand/aikya-mark.svg` | Primary full-color product mark used by the application and structured data |
| `frontend/public/brand/aikya-mark-mono.svg` | Single-color mask/pinned-tab-compatible mark |
| `frontend/public/favicon.svg` | Small-size browser identity derived from the primary mark |
| `frontend/public/site.webmanifest` | Installable web-app name, colors, and icon declaration |

The Phase 1 mark combines an A-shaped bridge with two paths meeting at one point. It expresses Aikya's “many languages, one understanding” idea without flags, a globe, a robot, or stereotyped scripts. Trademark and cultural review are still required before a public production launch.

## Social-image groups

All images are static 1200 × 630 JPEGs so crawlers do not depend on JavaScript or runtime image generation. They contain no customer data, unverified product claims, or third-party marks.

| Group | Asset | Routes |
|---|---|---|
| Product | `/og/aikya-product.jpg` | Home, features, pricing, authentication/private fallback metadata |
| Knowledge | `/og/aikya-knowledge.jpg` | Blog and documentation indexes and detail pages |
| Trust | `/og/aikya-trust.jpg` | About, contact, privacy, and terms |

Each public route still supplies its own title, description, canonical URL, and accessible image description. Image groups prevent near-identical binary files from being duplicated for routes with the same sharing purpose.

## Metadata contract

`usePageSeo()` is the single integration point for:

- page title and description;
- canonical URL;
- Open Graph title, description, type, URL, site name, locale, image URL, MIME type, dimensions, and alt text;
- X/Twitter large-card title, description, image, and image alt text;
- public crawl directives with large-image previews, or `noindex, nofollow` for private/authentication routes.

`frontend/app/seo/social-images.ts` owns the image registry. Route/page metadata chooses a registry key; components must not hardcode social-image paths.

The home page publishes truthful `Organization`, `WebSite`, and `SoftwareApplication` JSON-LD. The organization logo points to the crawlable primary SVG mark. Do not copy personal-portfolio or unrelated-business metadata into Aikya pages.

## Maintenance rules

1. Keep social artwork at 1200 × 630 and preferably below 200 KB.
2. Add a new image only when a route has a materially different sharing intent; otherwise reuse the nearest group.
3. Give every image a concise description of visible content, not promotional copy.
4. Never include secrets, user documents, account information, unverifiable compliance language, fake testimonials, or provider trademarks.
5. Update the registry and this route map together.
6. Validate rendered server HTML, absolute production image URLs, image HTTP responses, sitemap exclusion, and JSON-LD after SEO changes.
7. Keep previews static and lifecycle-free; no timer, observer, polling, or client-state ownership is required.

## Production validation

Set `NUXT_PUBLIC_SITE_URL` to the final HTTPS origin before building. After deployment, validate representative public pages with platform sharing debuggers and Google's Rich Results Test/Search Console. Localhost metadata is development-only and must never be used for a production build.
