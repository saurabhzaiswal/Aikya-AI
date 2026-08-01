export interface User {
  id: string
  email: string
  display_name: string
  locale: string
}

export interface UserContext {
  organization_id: string
  organization_name: string
  workspace_id: string
  workspace_name: string
}

export interface AuthResponse {
  access_token: string
  token_type: 'bearer'
  expires_in: number
  user: User
  context: UserContext
}

export interface ApiErrorPayload {
  error?: {
    code?: string
    message?: string
    request_id?: string | null
    retryable?: boolean
  }
}

export interface Language {
  code: string
  name: string
  direction: 'ltr' | 'rtl'
}

export interface TextTranslation {
  id: string
  source_language: string
  detected_language: string | null
  target_language: string
  source_text: string
  translated_text: string
  created_at: string
}

export interface Job {
  id: string
  document_id: string
  state: string
  stage: string
  progress: number
  target_language: string
  error_code: string | null
  error_message: string | null
  output_file_id: string | null
  created_at: string
}

export interface DocumentItem {
  id: string
  title: string
  status: string
  page_count: number | null
  warning_code: string | null
  created_at: string
  latest_job: Job | null
}

export interface DashboardSummary {
  document_count: number
  text_translation_count: number
  recent_documents: DocumentItem[]
  recent_translations: TextTranslation[]
}

export interface UploadIntent {
  upload_id: string
  upload_url: string
  required_headers: Record<string, string>
}

export interface UploadComplete {
  document_id: string
}

export interface DownloadResponse {
  download_url: string
}
