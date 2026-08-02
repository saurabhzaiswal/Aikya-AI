import type { ApiClient } from './api'
import type { AuthenticationResponseJSON, RegistrationResponseJSON } from '@simplewebauthn/browser'
import type {
  AuthResponse,
  LoginResponse,
  User,
  WebAuthnOptionsResponse,
  WebAuthnRegistrationResponse,
  WebAuthnRequiredResponse,
  WebAuthnStatusResponse,
} from '~/types/api'

export class AuthService {
  constructor(private readonly api: ApiClient) {}

  refresh(): Promise<AuthResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/refresh' })
  }

  login(email: string, password: string): Promise<LoginResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/login', data: { email, password } })
  }

  verifyPasskeyLogin(challengeId: string, credential: AuthenticationResponseJSON): Promise<AuthResponse> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/auth/webauthn/authenticate/verify',
      data: { challenge_id: challengeId, credential },
    })
  }

  verifyRecoveryCode(challengeId: string, recoveryCode: string): Promise<AuthResponse> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/auth/webauthn/recovery/verify',
      data: { challenge_id: challengeId, recovery_code: recoveryCode },
    })
  }

  pendingGoogleMfa(): Promise<WebAuthnRequiredResponse> {
    return this.api.request({ method: 'GET', url: '/api/v1/auth/webauthn/oauth/options' })
  }

  webauthnStatus(): Promise<WebAuthnStatusResponse> {
    return this.api.request({ method: 'GET', url: '/api/v1/auth/webauthn/status' })
  }

  webauthnRegistrationOptions(): Promise<WebAuthnOptionsResponse> {
    return this.api.request({ method: 'POST', url: '/api/v1/auth/webauthn/register/options' })
  }

  verifyWebAuthnRegistration(
    challengeId: string,
    credential: RegistrationResponseJSON,
  ): Promise<WebAuthnRegistrationResponse> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/auth/webauthn/register/verify',
      data: { challenge_id: challengeId, credential },
    })
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
