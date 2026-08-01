# PostgreSQL container assets

This folder is reserved for reviewed PostgreSQL initialization or configuration assets. Schema creation belongs to Alembic migrations once backend implementation begins; do not place ad-hoc production DDL here.

The foundation Compose files use the official PostgreSQL image, a named data volume, and `pg_isready` health checks. Production should prefer a managed, encrypted, backed-up PostgreSQL service when the hosting platform is selected.
