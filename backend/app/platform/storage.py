from dataclasses import dataclass
from typing import Any, cast

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.config import get_settings
from app.platform.errors import AppError


@dataclass(frozen=True)
class StoredObjectInfo:
    size: int
    content_type: str


class StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        common: dict[str, Any] = {
            "aws_access_key_id": settings.STORAGE_ACCESS_KEY,
            "aws_secret_access_key": settings.STORAGE_SECRET_KEY,
            "region_name": settings.STORAGE_REGION,
            "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        }
        self._internal = boto3.client("s3", endpoint_url=settings.STORAGE_ENDPOINT, **common)
        self._public = boto3.client("s3", endpoint_url=settings.STORAGE_PUBLIC_ENDPOINT, **common)
        self.settings = settings

    def create_upload_url(self, bucket: str, key: str, content_type: str) -> str:
        return cast(
            str,
            self._public.generate_presigned_url(
                "put_object",
                Params={"Bucket": bucket, "Key": key, "ContentType": content_type},
                ExpiresIn=self.settings.SIGNED_URL_TTL_SECONDS,
            ),
        )

    def create_download_url(self, bucket: str, key: str, filename: str) -> str:
        safe_name = filename.replace('"', "").replace("\r", "").replace("\n", "")
        return cast(
            str,
            self._public.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket,
                    "Key": key,
                    "ResponseContentDisposition": f'attachment; filename="{safe_name}"',
                },
                ExpiresIn=self.settings.SIGNED_DOWNLOAD_TTL_SECONDS,
            ),
        )

    def inspect(self, bucket: str, key: str) -> StoredObjectInfo:
        try:
            response = self._internal.head_object(Bucket=bucket, Key=key)
            signature = self._internal.get_object(Bucket=bucket, Key=key, Range="bytes=0-4")[
                "Body"
            ].read()
        except (BotoCoreError, ClientError) as exc:
            raise AppError(
                "storage_object_unavailable",
                "The uploaded file could not be verified.",
                status_code=409,
                retryable=True,
            ) from exc
        if signature != b"%PDF-":
            raise AppError("invalid_pdf", "The uploaded file is not a valid PDF.", status_code=415)
        return StoredObjectInfo(
            size=int(response["ContentLength"]),
            content_type=str(response.get("ContentType") or "application/octet-stream"),
        )

    def get_bytes(self, bucket: str, key: str) -> bytes:
        try:
            return cast(bytes, self._internal.get_object(Bucket=bucket, Key=key)["Body"].read())
        except (BotoCoreError, ClientError) as exc:
            raise AppError(
                "storage_read_failed",
                "The file could not be read from private storage.",
                status_code=503,
                retryable=True,
            ) from exc

    def put_bytes(self, bucket: str, key: str, body: bytes, content_type: str) -> None:
        try:
            self._internal.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
        except (BotoCoreError, ClientError) as exc:
            raise AppError(
                "storage_write_failed",
                "The file could not be written to private storage.",
                status_code=503,
                retryable=True,
            ) from exc

    def delete(self, bucket: str, key: str) -> None:
        try:
            self._internal.delete_object(Bucket=bucket, Key=key)
        except (BotoCoreError, ClientError) as exc:
            raise AppError(
                "storage_delete_failed",
                "The private storage object could not be removed.",
                status_code=503,
                retryable=True,
            ) from exc


def get_storage_service() -> StorageService:
    return StorageService()
