import type { ComputedRef, Ref } from 'vue'
import {
  findUiLanguage,
  groupUiLanguages,
  type UiLanguage,
  type UiLanguageGroup,
  type UiLocaleCode,
} from '~/i18n/language-registry'
import { useAuthStore } from '~/stores/auth'

export interface LanguageDetectionNotice {
  kind: 'detected' | 'fallback'
  languageName: string
}

export interface LanguageGroupView {
  key: UiLanguageGroup
  languages: readonly UiLanguage[]
}

export interface LanguagePreferenceController {
  currentLanguage: ComputedRef<UiLanguage>
  groups: ComputedRef<LanguageGroupView[]>
  indianContext: ComputedRef<boolean>
  notice: Ref<LanguageDetectionNotice | null>
  applyAccountLocale: (code: string) => Promise<void>
  dismissNotice: () => void
  selectLocale: (code: UiLocaleCode) => Promise<void>
}

const ONE_YEAR_SECONDS = 60 * 60 * 24 * 365

export function useLanguageDetection(): LanguagePreferenceController {
  const nuxtApp = useNuxtApp()
  const { locale, setLocale } = nuxtApp.$i18n
  const browserLocale = useBrowserLocale(nuxtApp)
  const initialized = useCookie<string | null>('aikya_language_initialized', {
    default: () => null,
    maxAge: ONE_YEAR_SECONDS,
    sameSite: 'lax',
  })
  const notice = useState<LanguageDetectionNotice | null>('language-detection-notice', () => null)
  const browserLanguage = findUiLanguage(browserLocale)

  const currentLanguage = computed<UiLanguage>(() => (
    findUiLanguage(locale.value) ?? findUiLanguage('en')!
  ))
  const indianContext = computed<boolean>(() => (
    browserLocale?.toUpperCase().endsWith('-IN') === true
    || currentLanguage.value.group === 'indian'
    || currentLanguage.value.group === 'bihar'
  ))
  const groups = computed<LanguageGroupView[]>(() => groupUiLanguages(indianContext.value))

  // Nuxt i18n already resolves Accept-Language/navigator and the locale cookie.
  // This separate marker only controls the one-time, non-blocking explanation.
  if (import.meta.client && initialized.value === null) {
    notice.value = browserLanguage
      ? { kind: 'detected', languageName: currentLanguage.value.nativeName }
      : { kind: 'fallback', languageName: 'English' }
    initialized.value = '1'
  }

  async function applyAccountLocale(code: string): Promise<void> {
    const language = findUiLanguage(code)
    if (!language || locale.value === language.code) return
    initialized.value = '1'
    notice.value = null
    await setLocale(language.code as UiLocaleCode)
  }

  async function selectLocale(code: UiLocaleCode): Promise<void> {
    const language = findUiLanguage(code)
    if (!language) return
    initialized.value = '1'
    notice.value = null
    await setLocale(code)

    const auth = useAuthStore()
    if (auth.isAuthenticated) {
      try {
        await auth.updateLocale(code)
      }
      catch {
        // Keep this device's explicit choice if account synchronization is unavailable.
      }
    }
  }

  function dismissNotice(): void {
    notice.value = null
  }

  return {
    currentLanguage,
    groups,
    indianContext,
    notice,
    applyAccountLocale,
    dismissNotice,
    selectLocale,
  }
}
