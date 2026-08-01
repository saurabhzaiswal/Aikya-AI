import hashlib
import html
import logging
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

import fitz
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.modules.documents.models import Document, FileObject, ProcessingJob
from app.modules.translation.provider import get_translation_provider
from app.platform.errors import AppError
from app.platform.identifiers import new_uuid7
from app.platform.malware import MalwareScanner
from app.platform.storage import StorageService
from app.worker import celery_app

logger = logging.getLogger(__name__)


def split_text(text: str, limit: int = 3_000) -> list[str]:
    paragraphs = [part.strip() for part in text.splitlines() if part.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > limit:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(
                paragraph[index : index + limit] for index in range(0, len(paragraph), limit)
            )
        elif len(current) + len(paragraph) + 2 > limit:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


def render_readable_pdf(page_translations: list[str], target_language: str) -> bytes:
    output = fitz.open()
    for source_page, translated_text in enumerate(page_translations, start=1):
        remaining = translated_text
        part = 1
        while remaining:
            chunk = remaining[:2_500]
            remaining = remaining[2_500:]
            page = output.new_page(width=595, height=842)
            heading = f"Translated page {source_page}"
            if part > 1:
                heading += f" — continued {part}"
            content = (
                f"<h2>{html.escape(heading)}</h2>"
                f'<p lang="{html.escape(target_language)}">'
                f"{html.escape(chunk).replace(chr(10), '<br>')}</p>"
            )
            page.insert_htmlbox(
                fitz.Rect(48, 42, 547, 800),
                content,
                css="body { font-family: sans-serif; font-size: 11pt; line-height: 1.45; } h2 { color: #4338ca; font-size: 14pt; }",
                scale_low=0.65,
            )
            part += 1
    if output.page_count == 0:
        raise AppError(
            "ocr_required", "This PDF does not contain extractable text.", status_code=422
        )
    value = cast(bytes, output.tobytes(garbage=4, deflate=True))
    output.close()
    return value


def update_job(
    db: Session,
    job: ProcessingJob,
    document: Document,
    *,
    state: str | None = None,
    stage: str | None = None,
    progress: int | None = None,
) -> None:
    if state is not None:
        job.state = state
        document.status = state
    if stage is not None:
        job.stage = stage
    if progress is not None:
        job.progress = progress
    db.commit()


@celery_app.task(name="aikya.documents.process_pdf", bind=True, max_retries=3)  # type: ignore[untyped-decorator]
def process_pdf(self, job_id: str) -> None:  # type: ignore[no-untyped-def]
    settings = get_settings()
    db = SessionLocal()
    try:
        job = db.get(ProcessingJob, UUID(job_id))
        if job is None or job.state == "completed":
            return
        document = db.get(Document, job.document_id)
        if document is None:
            return
        source = db.get(FileObject, document.source_file_id)
        if source is None:
            raise AppError(
                "source_file_missing", "The source file is unavailable.", status_code=409
            )

        job.started_at = datetime.now(UTC)
        update_job(db, job, document, state="processing", stage="validating", progress=5)
        storage = StorageService()
        source_bytes = storage.get_bytes(source.bucket, source.object_key)
        actual_checksum = hashlib.sha256(source_bytes).hexdigest()
        if actual_checksum != source.expected_checksum:
            raise AppError(
                "upload_checksum_mismatch",
                "The uploaded file failed integrity validation.",
                status_code=422,
            )

        MalwareScanner().scan(source_bytes)

        try:
            pdf = fitz.open(stream=source_bytes, filetype="pdf")
        except Exception as exc:
            raise AppError(
                "invalid_pdf", "The uploaded PDF could not be opened.", status_code=422
            ) from exc
        if pdf.needs_pass:
            pdf.close()
            raise AppError(
                "pdf_password_required",
                "Password-protected PDFs are not supported.",
                status_code=422,
            )
        if pdf.page_count > settings.MAX_DOCUMENT_PAGES:
            pdf.close()
            raise AppError(
                "pdf_page_limit_exceeded",
                f"PDF files are limited to {settings.MAX_DOCUMENT_PAGES} pages.",
                status_code=413,
            )

        page_texts = [page.get_text("text").strip() for page in pdf]
        page_count = pdf.page_count
        pdf.close()
        if not any(page_texts):
            raise AppError(
                "ocr_required",
                "This PDF appears to be scanned. OCR is planned for a later phase.",
                status_code=422,
            )

        source.actual_checksum = actual_checksum
        quarantine_location: tuple[str, str] | None = None
        if source.lifecycle_status != "clean":
            quarantine_location = (source.bucket, source.object_key)
            clean_key = f"{job.organization_id}/source/{source.id}.pdf"
            storage.put_bytes(
                settings.STORAGE_BUCKET_DOCUMENTS,
                clean_key,
                source_bytes,
                "application/pdf",
            )
            source.bucket = settings.STORAGE_BUCKET_DOCUMENTS
            source.object_key = clean_key
            source.lifecycle_status = "clean"
        document.page_count = page_count
        update_job(db, job, document, stage="translating", progress=25)
        if quarantine_location is not None:
            try:
                storage.delete(*quarantine_location)
            except AppError:
                logger.warning("Quarantine cleanup deferred", extra={"job_id": job_id})

        provider = get_translation_provider()
        translated_pages: list[str] = []
        total_chunks = sum(max(1, len(split_text(text))) for text in page_texts if text)
        translated_chunks = 0
        for page_text in page_texts:
            if not page_text:
                translated_pages.append("")
                continue
            page_result: list[str] = []
            for chunk in split_text(page_text):
                result = provider.translate(chunk, "auto", job.target_language)
                page_result.append(result.translated_text)
                translated_chunks += 1
                job.progress = 25 + int((translated_chunks / max(total_chunks, 1)) * 50)
                db.commit()
            translated_pages.append("\n\n".join(page_result))

        update_job(db, job, document, stage="rendering", progress=80)
        output_bytes = render_readable_pdf(translated_pages, job.target_language)
        output_id = new_uuid7()
        output_key = f"{job.organization_id}/output/{output_id}.pdf"
        output_name = f"{document.title[:-4] if document.title.lower().endswith('.pdf') else document.title}-{job.target_language}.pdf"
        storage.put_bytes(
            settings.STORAGE_BUCKET_OUTPUTS, output_key, output_bytes, "application/pdf"
        )
        output = FileObject(
            id=output_id,
            organization_id=job.organization_id,
            created_by=job.requested_by,
            purpose="output",
            bucket=settings.STORAGE_BUCKET_OUTPUTS,
            object_key=output_key,
            display_name=output_name,
            content_type="application/pdf",
            expected_size=len(output_bytes),
            actual_size=len(output_bytes),
            expected_checksum=hashlib.sha256(output_bytes).hexdigest(),
            actual_checksum=hashlib.sha256(output_bytes).hexdigest(),
            lifecycle_status="ready",
            expires_at=datetime.now(UTC) + timedelta(hours=settings.TEMPORARY_FILE_RETENTION_HOURS),
        )
        db.add(output)
        db.flush()
        job.output_file_id = output.id
        job.completed_at = datetime.now(UTC)
        document.warning_code = "basic_readable_export"
        update_job(db, job, document, state="completed", stage="completed", progress=100)
    except AppError as exc:
        db.rollback()
        if exc.retryable and self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=2 ** (self.request.retries + 1)) from exc
        job = db.get(ProcessingJob, UUID(job_id))
        if job is not None:
            document = db.get(Document, job.document_id)
            job.state = "failed"
            job.stage = "failed"
            job.error_code = exc.code
            job.error_message = exc.message
            job.completed_at = datetime.now(UTC)
            if document is not None:
                document.status = "failed"
                document.warning_code = exc.code
            db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("Document processing failed", extra={"job_id": job_id})
        job = db.get(ProcessingJob, UUID(job_id))
        if job is not None:
            document = db.get(Document, job.document_id)
            job.state = "failed"
            job.stage = "failed"
            job.error_code = "document_processing_failed"
            job.error_message = "The document could not be processed."
            job.completed_at = datetime.now(UTC)
            if document is not None:
                document.status = "failed"
            db.commit()
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=2 ** (self.request.retries + 1)) from exc
    finally:
        db.close()
