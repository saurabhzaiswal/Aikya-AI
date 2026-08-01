import type { ApiClient } from './api'
import type { AuthResponse, User } from '~/types/api'

export class AuthService {
  constructor(private readonly api: ApiClient) {}

  refresh(): Promise<AuthResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/refresh' })
  }

  login(email: string, password: string): Promise<AuthResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/login', data: { email, password } })
  }

  register(displayName: string, email: string, password: string, locale: string): Promise<AuthResponse> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/auth/register',
      data: { display_name: displayName, email, password, locale },
    })
  }

  updateLocale(locale: string): Promise<User> {
    return this.api.request({ method: 'PATCH', url: '/api/v1/auth/me/locale', data: { locale } })
  }

  logout(): Promise<void> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/logout' })
  }
}
