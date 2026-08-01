# ADR-016: Browser-First Language Preferences

Date: 2026-08-01  
Status: Accepted by founder instruction

## Problem

Aikya needs a welcoming language experience for global, Indian, and Bihar users without repeatedly overriding user choice, hardcoding regional rules in UI components, or collecting unnecessary location data.

## Options considered

1. English-only UI.
2. IP-country-first selection with a blocking first-visit modal.
3. Account/cookie/browser-first selection, a non-blocking notice, a permanent grouped switcher, and English catalog fallback.

## Decision

Use option 3. Account preference has highest priority, followed by the Nuxt locale cookie, SSR `Accept-Language`/client browser locale, and English. Country/IP lookup is not used in Phase 1. Detection is first-visit-only and never supersedes an explicit saved choice.

Maintain a central 23-locale registry and lazy catalogs. Keep all locales selectable; present Indian and Bihar groups first for Indian language context. Use Hindi then English fallback for Bhojpuri, Maithili, Bajjika, and Magahi, and English fallback elsewhere. Mark incomplete, unreviewed catalogs as Preview.

## Reasons

- Browser and account preferences represent user intent more accurately than IP country.
- No IP request or retained location is required.
- Nuxt i18n owns SSR detection, locale cookies, routing, and catalog fallback.
- A registry and composable keep policy out of page components and are reusable by later clients.
- Preview labels prevent partial catalogs from being misrepresented as production-complete translations.

## Consequences

- Users always retain manual control through the navigation switcher.
- Authenticated locale changes are stored in `users.locale` through a dedicated endpoint.
- Complete native-speaker translation review remains required before non-English locales become Live.
- Desktop/mobile reuse is an architectural provision, not authorization to implement future-phase clients now.

