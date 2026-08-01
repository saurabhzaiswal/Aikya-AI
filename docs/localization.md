# Localization Architecture

Last updated: 2026-08-01

## Scope

Phase 1 exposes one reusable UI-language registry for the Nuxt website and workspace. Future desktop/mobile clients may consume the same contract, but those clients are outside Phase 1 and are not implemented here.

The selector contains 23 standards-based locales:

- Global: English, Spanish, French, German, Arabic, Japanese, and Simplified Chinese.
- Indian: Hindi, Bengali, Marathi, Tamil, Telugu, Gujarati, Urdu, Kannada, Odia, Malayalam, Punjabi, and Assamese.
- Bihar: Bhojpuri, Maithili, Bajjika, and Magahi.

English is the production-complete source and fallback catalog. Other locales are visibly marked Preview until their complete product copy has been professionally translated and reviewed; missing messages resolve through Nuxt i18n fallback rather than template-level English literals.

## Preference priority

1. Authenticated account preference (`users.locale`).
2. Explicit saved locale cookie (`aikya_locale`).
3. SSR `Accept-Language`, then browser locale after hydration.
4. Optional privacy-reviewed country signal in a future ADR.
5. English.

Detection runs only before a preference cookie exists. An explicit language change updates the Nuxt locale cookie and, when authenticated, `PATCH /api/v1/auth/me/locale`. Login and refresh reapply the account preference. A failed account sync never rolls back the device's explicit selection.

IP geolocation is deliberately not used in Phase 1. The application does not need to collect or retain location data to choose a useful first language.

## Regional presentation

All three groups remain available to every user. For an Indian browser tag (`*-IN`) or an active Indian/Bihar locale, the Indian and Bihar groups are presented before Global. This improves discovery for Bihar users without claiming that a browser locale proves a person's precise location.

Bhojpuri (`bho`), Maithili (`mai`), Bajjika (`vjk`), and Magahi (`mag`) fall back to Hindi and then English. All other incomplete catalogs fall back to English. Arabic and Urdu carry right-to-left metadata.

## Implementation boundaries

- Registry and group ordering: `frontend/app/i18n/language-registry.ts`.
- Detection and preference orchestration: `frontend/app/composables/useLanguageDetection.ts`.
- Catalog fallback: `frontend/i18n/i18n.config.ts`.
- Locale cookie and SSR detection: `frontend/nuxt.config.ts`.
- Visible selector and one-time notice: common components, never page components.
- Account persistence: identity module schema/service/router plus typed frontend auth service.

No component may hardcode country-to-language mappings, subscribe to global browser events, or create timers for this feature. The implementation uses computed state and framework-owned cookies only, so it introduces no listener/timer lifecycle that could leak.

## Adding or graduating a locale

1. Add or update one registry entry with a valid BCP 47 tag, ISO 639-3 identifier, direction, group, and status.
2. Add its lazy JSON catalog.
3. Obtain native-speaker review for product terminology, accessibility labels, plurals, and layout.
4. Verify route generation, SSR `lang`/`dir`, fallback behavior, keyboard navigation, and small-screen selector layout.
5. Change status from Preview to Live only after the catalog is complete and reviewed.

