import type { ApiClient } from './api'
import { ApiError } from './api'
import type { DownloadResponse, Job, UploadComplete, UploadIntent } from '~/types/api'

export class DocumentService {
  constructor(private readonly api: ApiClient) {}

  createUpload(file: File, checksum: string): Promise<UploadIntent> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/uploads',
      data: {
        filename: file.name,
        content_type: 'application/pdf',
        size: file.size,
        checksum_sha256: checksum,
      },
    })
  }

  async uploadToSignedUrl(intent: UploadIntent, file: File): Promise<void> {
    const response = await fetch(intent.upload_url, {
      method: 'PUT',
      headers: intent.required_headers,
      body: file,
    })
    if (!response.ok) throw new ApiError('The PDF upload could not be completed.', 'upload_failed', response.status)
  }

  completeUpload(uploadId: string): Promise<UploadComplete> {
    return this.api.request({ method: 'POST', url: `/api/v1/uploads/${uploadId}/complete` })
  }

  createTranslation(documentId: string, targetLanguage: string): Promise<Job> {
    return this.api.request({
      method: 'POST',
      url: `/api/v1/documents/${documentId}/translations`,
      headers: { 'Idempotency-Key': crypto.randomUUID() },
      data: { target_language: targetLanguage },
    })
  }

  getJob(jobId: string): Promise<Job> {
    return this.api.request({ method: 'GET', url: `/api/v1/jobs/${jobId}` })
  }

  getDownloadUrl(fileId: string): Promise<DownloadResponse> {
    return this.api.request({ method: 'POST', url: `/api/v1/files/${fileId}/download-url` })
  }
}
