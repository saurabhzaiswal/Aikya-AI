# ADR-001: Use Vue 3 Instead of React

Date: 2026-08-01  
Status: Accepted  
Decision authority: Founder

## Context

Aikya needs a maintainable web stack and future extension/mobile/desktop paths. Earlier exploration mentioned both React and Vue, while the founder explicitly selected the Vue ecosystem and already works with it.

## Options considered

1. Vue 3 + TypeScript + Vite.
2. React + Next.js.
3. Framework-neutral web components.

## Decision

Use the Vue 3 ecosystem with TypeScript, Pinia, Tailwind CSS, and SCSS. ADR-014 selects Nuxt 4 as the primary web framework and defines the narrow Composition API exception required for Nuxt route/SEO integration.

## Reason

It matches founder expertise, reduces solo-maintenance cost, supports the required SPA/dashboard experience, and can be reused conceptually across extension, Tauri, and Vue-based mobile clients.

## Consequences

- React/Next.js libraries and patterns are not introduced.
- Components, documentation, and hiring/contribution guidance target Vue.
- Marketing SSR/SSG and the authenticated application share the Nuxt deployment in Phase 1 under ADR-014.
- Stateful components use Options API; Nuxt framework integration follows the explicit ADR-014 exception.
