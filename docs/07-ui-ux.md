# UI and UX System

Status: Foundation design specification  
Experience target: calm, fast, trustworthy, multilingual

## UX principles

1. Keep the user's document and next action central.
2. Explain processing, fidelity, privacy, retention, and cost before commitment.
3. Treat partial success and warnings as first-class states.
4. Separate Translate from AI Improve/Explain so intent is never ambiguous.
5. Preserve user control: cancel, retry, compare, export, and delete are always discoverable.
6. Design mobile and RTL behavior with the desktop layout, not after it.
7. Use motion to explain state; never use it to manufacture progress.

The editable primary journey is [`diagrams/user-flow.excalidraw`](diagrams/user-flow.excalidraw).

## Design system

### Foundations

- Nuxt 4, Vue 3, TypeScript, Nuxt i18n, Tailwind CSS, SCSS, and accessible Reka UI/headless primitives.
- Semantic design tokens for color, surface, text, border, focus, spacing, radius, shadow, typography, motion, and z-index.
- Tokens-not raw color names-express roles: `surface-default`, `text-muted`, `action-primary`, `status-warning`.
- Light and dark themes share semantic contrast goals; dark mode is not color inversion.
- Script-aware font stacks and resilient line-height support Latin, Devanagari, Arabic, CJK, and other launch scripts.
- An 8-point spacing rhythm with smaller 4-point increments for compact controls.
- Motion durations are short and state-oriented; reduced-motion mode removes nonessential transitions.

### Core components

- Buttons, icon buttons, links, inputs, text areas, selects/comboboxes, checkboxes, switches, radios.
- Dialog, drawer, popover, tooltip, menu, tabs, accordion, toast, inline alert.
- App shell, top bar, side navigation, breadcrumbs, command/search surface.
- Data table/list, filter bar, pagination/load-more, empty state, skeleton, error state.
- File drop zone, upload item, document card/row, page thumbnail, format badge.
- Language selector with native/localized names, script direction, search, recent choices.
- Job progress timeline, stage label, duration, cancellation, retry, warning summary.
- Side-by-side document/segment viewer with synchronized navigation and accessible nonvisual alternative.
- Quota meter, plan badge, invoice row, usage chart, privacy/provider disclosure.

Every component documents keyboard behavior, accessible name, focus behavior, loading/disabled/destructive states, RTL, responsive behavior, and analytics event if any.

## Information architecture and pages

### Public

- SSR landing, features, about, contact, pricing-positioning, privacy/terms, blog foundation, and documentation/help.
- Sign up, sign in, email verification, recovery, OAuth callback.

### Authenticated application

- Onboarding: purpose, preferred languages, privacy/retention choice, first translation.
- Dashboard: recent documents, primary upload, current processing, allowance, helpful next step.
- Translate text: source/target editors, language detection, provider/privacy tier, result actions.
- Upload/create: file selection, format/size validation, source/target, quality/privacy/retention summary, estimate.
- Processing: durable stage, progress, elapsed context, cancel, background navigation.
- Result: preview, source/target comparison, warnings, output formats, export, save/delete.
- Documents/history: list/grid, filters, folders, status, retention, bulk action later.
- Usage/billing: allowance, reservations, trend, plan, invoices, payment management.
- Organization/team: members, roles, invitations, organization policy.
- Settings: profile, sessions, language, theme, translation defaults, notifications, privacy/data, API later.
- Help/support: request ID/job ID guidance without encouraging content sharing.

### Admin

Admin is a separate restricted surface. It displays safe metadata and operational actions; document-content access is absent by default. Privileged action requires reason and audit.

## Dashboard layout

Desktop uses a collapsible left navigation, a contextual top bar, and a centered content area. The primary upload/translate action is visible without scrolling. Recent documents and active jobs favor a list for state clarity. Usage is secondary until nearing a limit.

On mobile, navigation becomes a drawer or bottom set limited to primary destinations. Upload action remains prominent. Dense tables become cards with the same information priority. Desktop hover actions gain persistent or menu equivalents.

## Primary user journey

1. Landing explains supported fidelity and privacy; user signs up.
2. Onboarding selects UI and target languages plus retention preference.
3. Dashboard presents upload and plain-text options.
4. Upload immediately validates local size/type, then securely transfers.
5. Review screen shows detected format, target language, fidelity expectation, external provider disclosure, retention, and estimated allowance.
6. Processing screen shows real stages and permits navigation away/cancellation.
7. Completion leads to result preview, warnings, comparison, and export.
8. User can save, delete, translate again, or review plan when limits justify it.

## Authentication experience

Login and registration use a responsive split-screen layout on large displays and a focused single-column form on small displays. Every field has an explicit label, useful placeholder, keyboard/autocomplete metadata, visible focus, `aria-invalid`, and a nearby error message. Registration mirrors the backend password contract with an 8–128 character checklist, three-of-four character-class requirement, confirmation field, and legal links.

Request errors remain visible inline and are also announced through a bounded global toast viewport. Toasts do not auto-dismiss, create timers, or grow without limit. Authentication calls retain the existing rotating HttpOnly refresh session and memory-only access token model. Social sign-in controls appear only when a real provider flow is configured; planned providers are never presented as working actions.

## Critical state design

- **Empty:** explain value and one next action.
- **Uploading:** bytes/progress, pause/resume only if supported, cancel, connection recovery.
- **Queued:** honest position/expectation without invented percentage.
- **Processing:** named stage and page/unit progress where measurable.
- **Partial:** downloadable readable result plus highlighted pages/segments needing review.
- **Retryable failure:** what failed, whether allowance was charged, retry action.
- **Permanent/unsupported:** clear reason and supported alternative.
- **Expired/deleted:** no broken download; explain lifecycle and recovery if available.
- **Quota blocked:** existing data stays accessible; show reset/upgrade/contact options.

## Translation and comparison experience

Side-by-side view synchronizes pages/segments without relying only on color. Selecting a segment reveals source, target, confidence/warnings, and later user correction. Long text, RTL/LTR mixing, tables, and vertical page navigation must not cause focus traps.

AI actions create a distinct proposed version labeled by action. Users can compare it with the direct translation, accept/export it, or discard it. The UI never silently replaces text with AI-improved content.

## Mobile experience

- File picker and camera entry are touch-friendly; camera is a later feature with explicit permission rationale.
- Preview uses one pane with a source/translation toggle; larger screens can split.
- Long-running jobs survive backgrounding through durable server state.
- Controls meet touch-target guidance and avoid critical actions at unsafe screen edges.
- Slow networks receive progress, retry, and no-duplicate submission behavior.

## Dark mode

Honor system preference initially and persist user override. Test every semantic token, document canvas, code/status badge, chart, focus ring, disabled control, and embedded preview. Source documents remain visually accurate; the surrounding canvas adapts without transforming the content.

## Accessibility

- Target WCAG 2.2 AA.
- Semantic landmarks/headings and logical focus order.
- Full keyboard operation with visible focus and skip navigation.
- Accessible names/instructions/errors tied to fields.
- Job progress announced at meaningful intervals through polite live regions, not on every percentage change.
- Status has icon/text in addition to color.
- Dialog focus is trapped/restored correctly; toast content is available through persistent history when important.
- Minimum contrast, zoom to 200%, responsive reflow, reduced motion, and screen-reader tests.
- Language attributes change for source/translated passages; RTL direction is set at content container level.
- Scrollbars use the centralized brand, brand-strong, and subtle design tokens with native Firefox and WebKit implementations; they remain visible, rounded, theme-aware, and do not hide overflow affordances.
- Primary and secondary actions expose a pointer cursor, hover elevation, pressed scale, and CSS-only ripple feedback. Reduced-motion preferences disable ripple animation. Critical authentication CTAs use locale-aware `NuxtLink` targets, and login/register pages remain directly reachable instead of redirecting based on stale client auth state.

## SEO and rendering

- Every public route has a unique title, description, canonical URL, Open Graph/Twitter metadata, crawl policy, and appropriate structured data.
- Public page meaning must exist in server-rendered HTML; critical copy cannot depend on client hydration.
- Authentication and `/app/**` routes are noindex and client-rendered so private session state is never serialized into public HTML.
- Sitemap and robots output contain only intended public routes. Programmatic and localized SEO routes remain architecture-ready, not generated without reviewed content.

## Localization

All UI strings use message keys with interpolation and plural rules. Never concatenate translated fragments. Language names appear in the user's UI locale plus native form when useful. Dates/numbers/currency use locale libraries; database/API values remain canonical. Screenshots and pseudo-localization test expansion before real localization.

English is the complete fallback catalog. Missing translated keys fall back through Nuxt i18n rather than ad hoc template expressions such as `translatedValue || 'English text'`, because missing-key behavior and plural/interpolation rules must remain centralized. Phase 1 exposes the 23-locale Global/Indian/Bihar registry described in [`localization.md`](localization.md); incomplete catalogs are marked Preview until native-speaker review.

Frontend lifecycle resources follow [`frontend-memory-safety.md`](frontend-memory-safety.md). Unexplained retained components, detached DOM nodes, orphan listeners/timers, unbounded stores/caches, or monotonic heap growth are release blockers.

## UX success measures

- Time and steps to first successful output.
- Upload abandonment and unsupported-file recovery.
- Job completion, cancellation, retry, and warning-review rates.
- Export success and repeat use.
- Accessibility defects and keyboard/screen-reader completion.
- User correction effort and confidence in privacy/fidelity explanations.
