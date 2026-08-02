import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const auth = useAuthStore()
  const localePath = useLocalePath()
  await auth.initialize()
  if (!auth.isAuthenticated) {
    return navigateTo({ path: localePath('/login'), query: { redirect: to.fullPath } })
  }
})
