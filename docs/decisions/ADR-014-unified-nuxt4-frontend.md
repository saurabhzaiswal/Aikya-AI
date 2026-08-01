# ADR-014: Use One Nuxt 4 Application for the Phase 1 Web Product

Date: 2026-08-01  
Status: Accepted  
Decision authority: Founder

## Context

Aikya needs crawlable public pages, structured metadata, international-SEO foundations, and the existing authenticated translation workspace. The product is operated by a solo founder, so separate marketing and dashboard applications would duplicate design, dependencies, deployment, and authentication integration during MVP.

## Options considered

1. One Nuxt 4 application using SSR/prerendering for public routes and client-side rendering for private `/app/**` routes.
2. Separate Nuxt marketing and Vue/Vite dashboard applications.
3. Keep the Vue/Vite SPA and add static marketing pages separately.

## Decision

Use one Nuxt 4 + Vue 3 + TypeScript application in `frontend/`. Follow Nuxt 4's `app/` source-directory convention. Public marketing/legal/content routes are server-rendered and SEO-enabled; authenticated `/app/**` routes are noindex and client-rendered because browser refresh credentials are path-scoped and must not be serialized into SSR state. FastAPI remains the only business API.

Use Pinia, Axios, Tailwind CSS 4, SCSS, VueUse, Nuxt SEO, Nuxt Content, Reka UI primitives, and reviewed shadcn-vue-style open-code UI components. Do not add a second frontend application or monorepo package layer until a later client creates measured reuse.

Nuxt route macros, SEO/content composables, plugins, and thin page shells may use Composition API where required by the framework. Stateful feature and design-system components continue to use the Vue Options API.

## Reason

This produces indexable HTML and one coherent design/deployment surface while preserving the working Phase 1 dashboard and the founder's Vue expertise. Hybrid rendering prevents private application state from becoming an SSR concern.

## Consequences

- ADR-001 remains valid for Vue over React; this ADR replaces its Vite-primary and Options-API-without-framework-exception details.
- Production serves a Nitro Node process instead of static Nginx files; edge Nginx continues to route traffic.
- Public routes require canonical metadata and structured data; private/auth routes require `noindex`.
- The browser access token remains in memory and refresh cookie remains HttpOnly; no token enters local storage or Nuxt payload state.
- A later website/dashboard split, internationalized routes, or shared packages require evidence and a new ADR.
