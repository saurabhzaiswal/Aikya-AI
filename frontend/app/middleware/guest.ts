import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async () => {
  if (import.meta.server) return

  const auth = useAuthStore()
  await auth.initialize()
  if (auth.isAuthenticated) return navigateTo('/app/dashboard')
})
