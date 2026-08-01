import type { ApiClient } from './api'
import type { DashboardSummary } from '~/types/api'

export class DashboardService {
  constructor(private readonly api: ApiClient) {}

  getSummary(): Promise<DashboardSummary> {
    return this.api.request({ method: 'GET', url: '/api/v1/dashboard/summary' })
  }
}
