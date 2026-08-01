import { defineStore } from 'pinia'

import type { AuthResponse, User, UserContext } from '~/types/api'

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
    applyAuth(auth: AuthResponse): void {
      useNuxtApp().$services.api.setAccessToken(auth.access_token)
      this.user = auth.user
      this.context = auth.context
    },
    clearAuth(): void {
      useNuxtApp().$services.api.setAccessToken(null)
      this.user = null
      this.context = null
    },
    async initialize(): Promise<void> {
      if (this.initialized) return
      try {
        this.applyAuth(await useNuxtApp().$services.auth.refresh())
      }
      catch {
        this.clearAuth()
      }
      finally {
        this.initialized = true
      }
    },
    async login(email: string, password: string): Promise<void> {
      this.applyAuth(await useNuxtApp().$services.auth.login(email, password))
      this.initialized = true
    },
    async register(displayName: string, email: string, password: string): Promise<void> {
      this.applyAuth(await useNuxtApp().$services.auth.register(displayName, email, password))
      this.initialized = true
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
