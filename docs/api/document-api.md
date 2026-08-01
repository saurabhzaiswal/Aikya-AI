# Document API Contract — Phase 1

Base path: `/api/v1`

Phase 1 supports digital PDFs with embedded text. OCR/scanned reconstruction is explicitly excluded.

## Upload flow

### `POST /uploads`

Accepts display filename, `application/pdf`, expected byte length, and SHA-256 checksum. After tenant/limit checks, returns an upload ID, short-lived signed PUT URL, required headers, and expiry.

### `POST /uploads/{upload_id}/complete`

Verifies object ownership, size, and MIME signature before creating immutable file/document metadata. The isolated processing worker then verifies the full SHA-256 checksum, scans through clamd, validates PDF structure/password state/embedded text/page limit, and only then promotes the source from quarantine. Completion is idempotent.

## Documents

- `GET /documents`: cursor-ready tenant-scoped list; Phase 1 may expose a bounded first page.
- `GET /documents/{document_id}`: metadata, current job/run, warnings, output.
- `POST /documents/{document_id}/translations`: starts an idempotent translation job with target language.
- Document deletion is required before private beta but is not part of the first Phase 1 implementation cut.
- `POST /files/{file_id}/download-url`: authorizes and returns a short-lived output URL.

## Job contract

`GET /jobs/{job_id}` returns state, public stage, monotonic progress, safe error code/message, retryable/cancellable flags, and output reference. Completion requires a validated output file record.

## Validation limits

Default 50 MB and 100 pages, configurable downward. Validate `%PDF-` signature, SHA-256, malware result, parser success, encryption/password state, embedded-text availability, and resource limits. Scanner outage fails closed and is retried; infected files never enter parsing. Never trust filename, browser MIME, or object key as authorization.
