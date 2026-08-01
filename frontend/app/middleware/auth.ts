import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const auth = useAuthStore()
  await auth.initialize()
  if (!auth.isAuthenticated) {
    return navigateTo({ path: '/login', query: { redirect: to.fullPath } })
  }
})
