import axios from 'axios'
import type { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

import type { ApiErrorPayload, AuthResponse } from '~/types/api'

interface RetriableRequest extends InternalAxiosRequestConfig {
  _authenticationRetried?: boolean
}

export class ApiError extends Error {
  code: string
  status: number
  requestId: string | null

  constructor(message: string, code = 'request_failed', status = 0, requestId: string | null = null) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
    this.requestId = requestId
  }
}

export class ApiClient {
  private readonly http: AxiosInstance
  private readonly refreshHttp: AxiosInstance
  private accessToken: string | null = null
  private refreshPromise: Promise<string | null> | null = null

  constructor(baseURL = '') {
    this.http = axios.create({ baseURL, withCredentials: true, timeout: 30_000 })
    this.refreshHttp = axios.create({ baseURL, withCredentials: true, timeout: 30_000 })
    this.http.interceptors.request.use((config) => {
      if (this.accessToken) config.headers.Authorization = `Bearer ${this.accessToken}`
      return config
    })
    this.http.interceptors.response.use(
      response => response,
      async (error: AxiosError<ApiErrorPayload>) => this.handleFailure(error),
    )
  }

  setAccessToken(token: string | null): void {
    this.accessToken = token
  }

  async request<T>(config: Parameters<AxiosInstance['request']>[0]): Promise<T> {
    const response = await this.http.request<T>(config)
    return response.data
  }

  private async refreshAccessToken(): Promise<string | null> {
    if (!this.refreshPromise) {
      this.refreshPromise = this.refreshHttp
        .post<AuthResponse>('/api/v1/auth/refresh')
        .then(({ data }) => {
          this.setAccessToken(data.access_token)
          return data.access_token
        })
        .catch(() => null)
        .finally(() => {
          this.refreshPromise = null
        })
    }
    return this.refreshPromise
  }

  private async handleFailure(error: AxiosError<ApiErrorPayload>): Promise<AxiosResponse> {
    const request = error.config as RetriableRequest | undefined
    const isRefreshRequest = request?.url === '/api/v1/auth/refresh'

    if (error.response?.status === 401 && request && !request._authenticationRetried && !isRefreshRequest) {
      request._authenticationRetried = true
      if (await this.refreshAccessToken()) return this.http.request(request).then(response => response)
    }

    const payload = error.response?.data
    throw new ApiError(
      payload?.error?.message || 'The request could not be completed.',
      payload?.error?.code || 'request_failed',
      error.response?.status || 0,
      payload?.error?.request_id || (error.response?.headers['x-request-id'] as string | undefined) || null,
    )
  }
}
