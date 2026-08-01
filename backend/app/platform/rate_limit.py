import hashlib

from redis import Redis
from redis.exceptions import RedisError

from app.config import get_settings
from app.platform.errors import AppError


def check_rate_limit(bucket: str, identity: str, *, limit: int, window_seconds: int) -> None:
    settings = get_settings()
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    key = f"rate:{bucket}:{digest}"
    client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        with client.pipeline(transaction=True) as pipeline:
            pipeline.incr(key)
            pipeline.expire(key, window_seconds, nx=True)
            count, _ = pipeline.execute()
    except RedisError as exc:
        if settings.AIKYA_ENV == "production":
            raise AppError(
                "rate_limit_unavailable",
                "This request cannot be accepted right now. Please try again shortly.",
                status_code=503,
                retryable=True,
            ) from exc
        return
    finally:
        client.close()
    if int(count) > limit:
        raise AppError(
            "rate_limit_exceeded",
            "Too many requests. Please wait and try again.",
            status_code=429,
            retryable=True,
        )
