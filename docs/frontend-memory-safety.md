# Frontend Memory Safety

Status: Mandatory engineering policy  
Applies to: Nuxt/Vue browser runtime, SSR runtime, Pinia stores, composables, and UI integrations

Memory leaks are release-blocking defects. No engineer can truthfully guarantee that a complex browser application will never leak under every runtime condition, so Aikya enforces prevention, bounded ownership, profiling, and regression gates instead of making an unverifiable claim.

## Ownership rules

- Every event listener, observer, subscription, timer, animation frame, worker, stream, socket, and polling loop has one named owner and a matching cleanup path.
- Options API components release resources in `beforeUnmount`/`unmounted`; scoped Nuxt composables use `onScopeDispose` or `onUnmounted`.
- Requests that can outlive their view use `AbortController`/Axios cancellation and ignore stale responses after teardown.
- Polling is non-overlapping, stops on terminal state and route teardown, backs off when appropriate, and never recursively creates unmanaged timers.
- Blob/object URLs are revoked; large buffers, document previews, detached DOM references, and provider SDK objects are released after use.
- Pinia stores expose bounded state and clear user/tenant-sensitive state on logout or tenant change. Unbounded histories and caches are forbidden.
- SSR code never stores request/user mutable state in module-level singletons. Per-request state stays within Nuxt request scope.
- Third-party libraries must document teardown behavior before adoption. A dependency that cannot be disposed safely is not accepted.

## Review checklist

For every frontend change, review all lifecycle-producing APIs: `addEventListener`, timers, watchers, observers, subscriptions, sockets, object URLs, async requests, and third-party instances. Confirm cleanup runs on normal unmount, navigation, failed initialization, logout, and repeated mount/unmount cycles.

## Verification gate

- ESLint/type/build checks remain mandatory.
- Polling and listener code receives explicit lifecycle review.
- Before private beta and after material dashboard/document-viewer changes, profile repeated navigation and representative long-running workflows with browser heap snapshots/allocation timelines.
- Investigate retained component instances, detached DOM trees, growing listener/timer counts, and memory that does not return after garbage collection.
- Record the scenario, browser/build, baseline, repeated-cycle result, and accepted bound. Any unexplained monotonic growth blocks release.

The current PDF polling component owns one timeout, prevents overlapping timers, and clears it during `beforeUnmount`. New asynchronous UI must follow the same ownership pattern.

The `v-wave` package was evaluated for project-wide button ripple effects on 2026-08-02. Its distributed Vue directive attaches pointer/click listeners without an explicit directive unmount hook, so it was not retained. Aikya uses CSS-only shared ripple classes instead; they allocate no component lifecycle resource and honor `prefers-reduced-motion`.
