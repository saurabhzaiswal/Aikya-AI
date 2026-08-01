from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class UploadIntentRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str
    size: int = Field(gt=0)
    checksum_sha256: str = Field(min_length=64, max_length=64)

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str) -> str:
        normalized = value.lower()
        if any(char not in "0123456789abcdef" for char in normalized):
            raise ValueError("Checksum must be hexadecimal SHA-256")
        return normalized


class UploadIntentResponse(BaseModel):
    upload_id: UUID
    upload_url: str
    method: str = "PUT"
    required_headers: dict[str, str]
    expires_in: int


class UploadCompleteResponse(BaseModel):
    document_id: UUID
    status: str


class DocumentTranslationRequest(BaseModel):
    target_language: str = Field(min_length=2, max_length=35)


class JobResponse(BaseModel):
    id: UUID
    document_id: UUID
    state: str
    stage: str
    progress: int
    target_language: str
    error_code: str | None
    error_message: str | None
    output_file_id: UUID | None
    created_at: datetime


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    status: str
    page_count: int | None
    warning_code: str | None
    created_at: datetime
    latest_job: JobResponse | None = None


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]


class DownloadUrlResponse(BaseModel):
    download_url: str
    expires_in: int
