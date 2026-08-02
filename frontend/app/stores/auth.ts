import { defineStore } from 'pinia'

import type { AuthenticationResponseJSON } from '@simplewebauthn/browser'
import type { AuthResponse, User, UserContext, WebAuthnRequiredResponse } from '~/types/api'

interface AuthState {
  user: User | null
  context: UserContext | null
  initialized: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({ user: null, context: null, initialized: false }),
  getters: {
    isAuthenticated: (state): boolean => Boolean(state.user),
  },
  actions: {
    async applyAuth(auth: AuthResponse): Promise<void> {
      useNuxtApp().$services.api.setAccessToken(auth.access_token)
      this.user = auth.user
      this.context = auth.context
      try {
        await useNuxtApp().$languagePreference.applyAccountLocale(auth.user.locale)
      }
      catch {
        // Authentication remains valid if optional locale synchronization fails.
      }
    },
    clearAuth(): void {
      useNuxtApp().$services.api.setAccessToken(null)
      this.user = null
      this.context = null
    },
    async initialize(): Promise<void> {
      if (this.initialized) return
      try {
        await this.applyAuth(await useNuxtApp().$services.auth.refresh())
      }
      catch {
        this.clearAuth()
      }
      finally {
        this.initialized = true
      }
    },
    async login(email: string, password: string): Promise<WebAuthnRequiredResponse | null> {
      const result = await useNuxtApp().$services.auth.login(email, password)
      if ('status' in result && result.status === 'mfa_required') {
        return result as WebAuthnRequiredResponse
      }
      await this.applyAuth(result as AuthResponse)
      this.initialized = true
      return null
    },
    async completePasskeyLogin(challengeId: string, credential: AuthenticationResponseJSON): Promise<void> {
      await this.applyAuth(await useNuxtApp().$services.auth.verifyPasskeyLogin(challengeId, credential))
      this.initialized = true
    },
    async completeRecoveryLogin(challengeId: string, recoveryCode: string): Promise<void> {
      await this.applyAuth(await useNuxtApp().$services.auth.verifyRecoveryCode(challengeId, recoveryCode))
      this.initialized = true
    },
    async register(displayName: string, email: string, password: string, locale: string): Promise<void> {
      await this.applyAuth(await useNuxtApp().$services.auth.register(displayName, email, password, locale))
      this.initialized = true
    },
    async updateLocale(locale: string): Promise<void> {
      this.user = await useNuxtApp().$services.auth.updateLocale(locale)
    },
    async logout(): Promise<void> {
      try {
        await useNuxtApp().$services.auth.logout()
      }
      finally {
        this.clearAuth()
        this.initialized = true
      }
    },
  },
})
