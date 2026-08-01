import type { AikyaServices } from '~/services'

declare module '#app' {
  interface NuxtApp {
    $services: AikyaServices
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $services: AikyaServices
  }
}

export {}
