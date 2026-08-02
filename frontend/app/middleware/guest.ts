import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(() => {
  if (import.meta.server) return

  const auth = useAuthStore()
  const localePath = useLocalePath()
  // Guest forms must remain available when the API is starting or unavailable.
  // Private routes perform authoritative refresh-session initialization.
  if (auth.isAuthenticated) return navigateTo(localePath('/app/dashboard'))
})
