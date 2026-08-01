# Redis container assets

Redis carries transient cache, rate-limit, lock, and Celery transport data. It is not the source of truth for accepted jobs, usage, billing, or document state.

The reference configuration enables AOF persistence and disables eviction to avoid silent queue-key loss. Production authentication, TLS, backup, high availability, and memory sizing should come from the selected managed service rather than committing credentials here.
