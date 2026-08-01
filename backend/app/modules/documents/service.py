import re
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.modules.documents.models import Document, FileObject, ProcessingJob
from app.modules.documents.schemas import DocumentResponse, JobResponse, UploadIntentRequest
from app.modules.organizations.models import Workspace
from app.platform.errors import AppError
from app.platform.identifiers import new_uuid7
from app.platform.storage import StorageService


def safe_display_name(filename: str) -> str:
    value = filename.replace("\\", "/").split("/")[-1].strip()
    value = re.sub(r"[\x00-\x1f\x7f]", "", value)
    if not value or len(value) > 255:
        raise AppError("invalid_filename", "The filename is invalid.", status_code=422)
    return value


def create_upload_intent(
    db: Session,
    storage: StorageService,
    *,
    organization_id: UUID,
    user_id: UUID,
    payload: UploadIntentRequest,
) -> tuple[FileObject, str]:
    settings = get_settings()
    if payload.content_type != "application/pdf" or not payload.filename.lower().endswith(".pdf"):
        raise AppError("file_type_unsupported", "Phase 1 supports PDF files only.", status_code=415)
    if payload.size > settings.MAX_UPLOAD_BYTES:
        raise AppError(
            "file_too_large",
            f"PDF files are limited to {settings.MAX_UPLOAD_BYTES} bytes.",
            status_code=413,
        )
    file_id = new_uuid7()
    object_key = f"{organization_id}/source/{file_id}.pdf"
    record = FileObject(
        id=file_id,
        organization_id=organization_id,
        created_by=user_id,
        purpose="source",
        bucket=settings.STORAGE_BUCKET_QUARANTINE,
        object_key=object_key,
        display_name=safe_display_name(payload.filename),
        content_type=payload.content_type,
        expected_size=payload.size,
        expected_checksum=payload.checksum_sha256,
        expires_at=datetime.now(UTC) + timedelta(hours=settings.TEMPORARY_FILE_RETENTION_HOURS),
    )
    db.add(record)
    db.commit()
    return record, storage.create_upload_url(record.bucket, record.object_key, record.content_type)


def complete_upload(
    db: Session,
    storage: StorageService,
    *,
    organization_id: UUID,
    user_id: UUID,
    upload_id: UUID,
) -> Document:
    record = db.scalar(
        select(FileObject).where(
            FileObject.id == upload_id,
            FileObject.organization_id == organization_id,
            FileObject.created_by == user_id,
        )
    )
    if record is None:
        raise AppError("upload_not_found", "The upload was not found.", status_code=404)
    existing = db.scalar(select(Document).where(Document.source_file_id == record.id))
    if existing is not None:
        return existing
    if record.lifecycle_status != "pending_upload":
        raise AppError("upload_not_ready", "The upload is not ready.", status_code=409)
    info = storage.inspect(record.bucket, record.object_key)
    if info.size != record.expected_size:
        raise AppError(
            "upload_size_mismatch", "The uploaded file size does not match.", status_code=409
        )
    workspace = db.scalar(select(Workspace).where(Workspace.organization_id == organization_id))
    if workspace is None:
        raise AppError("workspace_unavailable", "The workspace is not available.", status_code=409)
    record.actual_size = info.size
    record.lifecycle_status = "uploaded"
    document = Document(
        organization_id=organization_id,
        workspace_id=workspace.id,
        created_by=user_id,
        source_file_id=record.id,
        title=record.display_name,
        status="uploaded",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def start_translation(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    document_id: UUID,
    target_language: str,
    idempotency_key: str,
) -> ProcessingJob:
    document = db.scalar(
        select(Document).where(
            Document.id == document_id, Document.organization_id == organization_id
        )
    )
    if document is None:
        raise AppError("document_not_found", "The document was not found.", status_code=404)
    existing = db.scalar(
        select(ProcessingJob).where(
            ProcessingJob.organization_id == organization_id,
            ProcessingJob.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        if existing.document_id != document_id or existing.target_language != target_language:
            raise AppError(
                "idempotency_conflict",
                "This idempotency key was already used for a different request.",
                status_code=409,
            )
        return existing
    job = ProcessingJob(
        organization_id=organization_id,
        document_id=document.id,
        requested_by=user_id,
        target_language=target_language,
        idempotency_key=idempotency_key,
    )
    document.status = "queued"
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, organization_id: UUID, job_id: UUID) -> ProcessingJob:
    job = db.scalar(
        select(ProcessingJob).where(
            ProcessingJob.id == job_id, ProcessingJob.organization_id == organization_id
        )
    )
    if job is None:
        raise AppError("job_not_found", "The processing job was not found.", status_code=404)
    return job


def list_documents(db: Session, organization_id: UUID, limit: int = 30) -> list[DocumentResponse]:
    documents = db.scalars(
        select(Document)
        .where(Document.organization_id == organization_id)
        .order_by(Document.created_at.desc(), Document.id.desc())
        .limit(limit)
    ).all()
    results: list[DocumentResponse] = []
    for document in documents:
        latest_job = db.scalar(
            select(ProcessingJob)
            .where(
                ProcessingJob.document_id == document.id,
                ProcessingJob.organization_id == organization_id,
            )
            .order_by(ProcessingJob.created_at.desc())
            .limit(1)
        )
        results.append(to_document_response(document, latest_job))
    return results


def get_document(db: Session, organization_id: UUID, document_id: UUID) -> DocumentResponse:
    document = db.scalar(
        select(Document).where(
            Document.id == document_id, Document.organization_id == organization_id
        )
    )
    if document is None:
        raise AppError("document_not_found", "The document was not found.", status_code=404)
    latest_job = db.scalar(
        select(ProcessingJob)
        .where(ProcessingJob.document_id == document.id)
        .order_by(ProcessingJob.created_at.desc())
        .limit(1)
    )
    return to_document_response(document, latest_job)


def get_download_url(
    db: Session, storage: StorageService, organization_id: UUID, file_id: UUID
) -> str:
    record = db.scalar(
        select(FileObject).where(
            FileObject.id == file_id,
            FileObject.organization_id == organization_id,
            FileObject.lifecycle_status == "ready",
        )
    )
    if record is None or record.purpose != "output":
        raise AppError("file_not_found", "The output file was not found.", status_code=404)
    return storage.create_download_url(record.bucket, record.object_key, record.display_name)


def to_job_response(job: ProcessingJob) -> JobResponse:
    return JobResponse(
        id=job.id,
        document_id=job.document_id,
        state=job.state,
        stage=job.stage,
        progress=job.progress,
        target_language=job.target_language,
        error_code=job.error_code,
        error_message=job.error_message,
        output_file_id=job.output_file_id,
        created_at=job.created_at,
    )


def to_document_response(document: Document, job: ProcessingJob | None) -> DocumentResponse:
    return DocumentResponse(
        id=document.id,
        title=document.title,
        status=document.status,
        page_count=document.page_count,
        warning_code=document.warning_code,
        created_at=document.created_at,
        latest_job=to_job_response(job) if job else None,
    )
