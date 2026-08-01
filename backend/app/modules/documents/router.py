from uuid import UUID

from celery.exceptions import CeleryError
from fastapi import APIRouter, Depends, Header
from kombu.exceptions import KombuError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.modules.documents.schemas import (
    DocumentListResponse,
    DocumentResponse,
    DocumentTranslationRequest,
    DownloadUrlResponse,
    JobResponse,
    UploadCompleteResponse,
    UploadIntentRequest,
    UploadIntentResponse,
)
from app.modules.documents.service import (
    complete_upload,
    create_upload_intent,
    get_document,
    get_download_url,
    get_job,
    list_documents,
    start_translation,
    to_job_response,
)
from app.modules.identity.dependencies import CurrentPrincipal, get_current_principal
from app.platform.errors import AppError
from app.platform.rate_limit import check_rate_limit
from app.platform.storage import StorageService, get_storage_service
from app.worker import celery_app

router = APIRouter(tags=["documents"])


@router.post("/uploads", response_model=UploadIntentResponse, status_code=201)
def upload_intent(
    payload: UploadIntentRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
) -> UploadIntentResponse:
    check_rate_limit(
        "upload",
        str(principal.user.id),
        limit=get_settings().UPLOAD_RATE_LIMIT,
        window_seconds=get_settings().WORKLOAD_RATE_WINDOW_SECONDS,
    )
    record, url = create_upload_intent(
        db,
        storage,
        organization_id=principal.organization_id,
        user_id=principal.user.id,
        payload=payload,
    )
    return UploadIntentResponse(
        upload_id=record.id,
        upload_url=url,
        required_headers={"Content-Type": record.content_type},
        expires_in=get_settings().SIGNED_URL_TTL_SECONDS,
    )


@router.post("/uploads/{upload_id}/complete", response_model=UploadCompleteResponse)
def finish_upload(
    upload_id: UUID,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
) -> UploadCompleteResponse:
    document = complete_upload(
        db,
        storage,
        organization_id=principal.organization_id,
        user_id=principal.user.id,
        upload_id=upload_id,
    )
    return UploadCompleteResponse(document_id=document.id, status=document.status)


@router.get("/documents", response_model=DocumentListResponse)
def documents(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> DocumentListResponse:
    return DocumentListResponse(items=list_documents(db, principal.organization_id))


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def document_detail(
    document_id: UUID,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    return get_document(db, principal.organization_id, document_id)


@router.post("/documents/{document_id}/translations", response_model=JobResponse, status_code=202)
def translate_document(
    document_id: UUID,
    payload: DocumentTranslationRequest,
    idempotency_key: str = Header(min_length=8, max_length=120, alias="Idempotency-Key"),
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> JobResponse:
    job = start_translation(
        db,
        organization_id=principal.organization_id,
        user_id=principal.user.id,
        document_id=document_id,
        target_language=payload.target_language,
        idempotency_key=idempotency_key,
    )
    try:
        celery_app.send_task("aikya.documents.process_pdf", args=[str(job.id)])
    except (CeleryError, KombuError) as exc:
        raise AppError(
            "job_queue_unavailable",
            "The document was saved, but processing could not be queued. Retry shortly.",
            status_code=503,
            retryable=True,
        ) from exc
    return to_job_response(job)


@router.get("/jobs/{job_id}", response_model=JobResponse)
def job_status(
    job_id: UUID,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> JobResponse:
    return to_job_response(get_job(db, principal.organization_id, job_id))


@router.post("/files/{file_id}/download-url", response_model=DownloadUrlResponse)
def download_url(
    file_id: UUID,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
) -> DownloadUrlResponse:
    return DownloadUrlResponse(
        download_url=get_download_url(db, storage, principal.organization_id, file_id),
        expires_in=get_settings().SIGNED_DOWNLOAD_TTL_SECONDS,
    )
