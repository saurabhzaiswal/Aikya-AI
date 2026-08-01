"""Application-wide identifier generation policy."""

from uuid import UUID, uuid7


def new_uuid7() -> UUID:
    """Return a time-ordered UUIDv7 for persisted business identifiers."""

    return uuid7()
