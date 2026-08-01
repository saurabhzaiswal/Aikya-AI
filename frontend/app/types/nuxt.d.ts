import type { AikyaServices } from '~/services'
import type { LanguagePreferenceController } from '~/composables/useLanguageDetection'

declare module '#app' {
  interface NuxtApp {
    $services: AikyaServices
    $languagePreference: LanguagePreferenceController
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $services: AikyaServices
    $languagePreference: LanguagePreferenceController
  }
}

export {}
