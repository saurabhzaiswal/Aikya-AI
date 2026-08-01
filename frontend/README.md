# Aikya AI web application

The Phase 1 frontend is one Nuxt 4 application containing both the SSR public website and the client-rendered authenticated workspace.

Localization uses official Nuxt i18n with English as the complete fallback catalog and Hindi as the first additional locale. Frontend lifecycle work follows [`../docs/frontend-memory-safety.md`](../docs/frontend-memory-safety.md).

## Runtime boundaries

- Public pages use SSR or prerendering for accessible, indexable HTML.
- `/app/**`, `/login`, and `/register` run client-side and are excluded from search indexing.
- Authentication access tokens stay in browser memory. Refresh uses the backend's protected cookie flow.
- Stateful UI components use Vue 3 Options API. Thin Nuxt routes, middleware, plugins, and SEO/content composables may use Nuxt's Composition API primitives under ADR-014.

## Commands

```bash
npm install
npm run dev
npm run lint
npm run typecheck
npm run build
```

Node.js `>=24.18.0 <25` is required. Docker remains the supported full-stack workflow.
