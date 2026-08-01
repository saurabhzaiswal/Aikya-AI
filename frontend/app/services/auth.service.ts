import type { ApiClient } from './api'
import type { AuthResponse } from '~/types/api'

export class AuthService {
  constructor(private readonly api: ApiClient) {}

  refresh(): Promise<AuthResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/refresh' })
  }

  login(email: string, password: string): Promise<AuthResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/login', data: { email, password } })
  }

  register(displayName: string, email: string, password: string): Promise<AuthResponse> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/auth/register',
      data: { display_name: displayName, email, password },
    })
  }

  logout(): Promise<void> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/logout' })
  }
}
