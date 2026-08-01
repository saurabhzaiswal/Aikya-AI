import { createServices } from '~/services'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  return {
    provide: {
      services: createServices(config.public.apiBase),
    },
  }
})
