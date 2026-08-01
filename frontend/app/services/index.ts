import { ApiClient } from './api'
import { AuthService } from './auth.service'
import { DashboardService } from './dashboard.service'
import { DocumentService } from './document.service'
import { TranslationService } from './translation.service'

export function createServices(apiBase = '') {
  const api = new ApiClient(apiBase)
  return {
    api,
    auth: new AuthService(api),
    dashboard: new DashboardService(api),
    documents: new DocumentService(api),
    translation: new TranslationService(api),
  }
}

export type AikyaServices = ReturnType<typeof createServices>
