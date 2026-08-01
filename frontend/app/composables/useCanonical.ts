export function useCanonical(path?: string): string {
  const route = useRoute()
  const config = useRuntimeConfig()
  const canonical = new URL(path || route.path, config.public.siteUrl).toString()
  useHead({ link: [{ rel: 'canonical', href: canonical }] })
  return canonical
}
