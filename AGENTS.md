# Aikya AI Agent Rules

Before making any repository change:

1. Read `.agents/MASTER_CONTEXT.md` and `.agents/agent-instructions.md`.
2. Read `docs/PROJECT_STATUS.md` and `docs/project-progress.md`.
3. Read the relevant architecture, security, API, UX, and decision documents.
4. Follow ADR-014 Nuxt 4 rules, scoped Vue Options API rules, FastAPI modular-monolith, Docker, security, and documentation rules.
5. Work only within the explicitly approved phase and scope.
6. Update progress and documentation after completed work.
7. Treat frontend memory leaks as release-blocking defects; read `docs/frontend-memory-safety.md` before adding timers, listeners, observers, polling, sockets, object URLs, or long-lived client state.

Permanent baselines: Python 3.14+, Node.js 24.18.x, application-generated UUIDv7 persisted identifiers, and Nuxt i18n with English as the complete fallback locale. Do not weaken or replace these without founder approval and an ADR.
7. Treat frontend memory leaks as release-blocking defects; read `docs/frontend-memory-safety.md` before adding timers, listeners, observers, polling, sockets, object URLs, or long-lived client state.

Permanent baselines: Python 3.14+, Node.js 24.18.x, application-generated UUIDv7 persisted identifiers, and Nuxt i18n with English as the complete fallback locale. Do not weaken or replace these without founder approval and an ADR.

Detailed private operating instructions live in `.agents/` and are intentionally Git-ignored. Public engineering decisions live in `docs/`.
