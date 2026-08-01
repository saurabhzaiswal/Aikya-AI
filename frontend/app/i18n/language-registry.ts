export const UI_LANGUAGE_GROUPS = ['global', 'indian', 'bihar'] as const

export type UiLanguageGroup = typeof UI_LANGUAGE_GROUPS[number]
export type UiLanguageStatus = 'live' | 'preview'
export type TextDirection = 'ltr' | 'rtl'

interface UiLanguageDefinition {
  code: string
  language: string
  iso639_3: string
  englishName: string
  nativeName: string
  direction: TextDirection
  group: UiLanguageGroup
  status: UiLanguageStatus
}

export const UI_LANGUAGES = [
  { code: 'en', language: 'en', iso639_3: 'eng', englishName: 'English', nativeName: 'English', direction: 'ltr', group: 'global', status: 'live' },
  { code: 'es', language: 'es', iso639_3: 'spa', englishName: 'Spanish', nativeName: 'Español', direction: 'ltr', group: 'global', status: 'preview' },
  { code: 'fr', language: 'fr', iso639_3: 'fra', englishName: 'French', nativeName: 'Français', direction: 'ltr', group: 'global', status: 'preview' },
  { code: 'de', language: 'de', iso639_3: 'deu', englishName: 'German', nativeName: 'Deutsch', direction: 'ltr', group: 'global', status: 'preview' },
  { code: 'ar', language: 'ar', iso639_3: 'ara', englishName: 'Arabic', nativeName: 'العربية', direction: 'rtl', group: 'global', status: 'preview' },
  { code: 'ja', language: 'ja', iso639_3: 'jpn', englishName: 'Japanese', nativeName: '日本語', direction: 'ltr', group: 'global', status: 'preview' },
  { code: 'zh', language: 'zh-Hans', iso639_3: 'zho', englishName: 'Chinese (Simplified)', nativeName: '简体中文', direction: 'ltr', group: 'global', status: 'preview' },
  { code: 'hi', language: 'hi-IN', iso639_3: 'hin', englishName: 'Hindi', nativeName: 'हिन्दी', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'bn', language: 'bn-IN', iso639_3: 'ben', englishName: 'Bengali', nativeName: 'বাংলা', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'mr', language: 'mr-IN', iso639_3: 'mar', englishName: 'Marathi', nativeName: 'मराठी', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'ta', language: 'ta-IN', iso639_3: 'tam', englishName: 'Tamil', nativeName: 'தமிழ்', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'te', language: 'te-IN', iso639_3: 'tel', englishName: 'Telugu', nativeName: 'తెలుగు', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'gu', language: 'gu-IN', iso639_3: 'guj', englishName: 'Gujarati', nativeName: 'ગુજરાતી', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'ur', language: 'ur-IN', iso639_3: 'urd', englishName: 'Urdu', nativeName: 'اردو', direction: 'rtl', group: 'indian', status: 'preview' },
  { code: 'kn', language: 'kn-IN', iso639_3: 'kan', englishName: 'Kannada', nativeName: 'ಕನ್ನಡ', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'or', language: 'or-IN', iso639_3: 'ori', englishName: 'Odia', nativeName: 'ଓଡ଼ିଆ', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'ml', language: 'ml-IN', iso639_3: 'mal', englishName: 'Malayalam', nativeName: 'മലയാളം', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'pa', language: 'pa-IN', iso639_3: 'pan', englishName: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'as', language: 'as-IN', iso639_3: 'asm', englishName: 'Assamese', nativeName: 'অসমীয়া', direction: 'ltr', group: 'indian', status: 'preview' },
  { code: 'bho', language: 'bho-IN', iso639_3: 'bho', englishName: 'Bhojpuri', nativeName: 'भोजपुरी', direction: 'ltr', group: 'bihar', status: 'preview' },
  { code: 'mai', language: 'mai-IN', iso639_3: 'mai', englishName: 'Maithili', nativeName: 'मैथिली', direction: 'ltr', group: 'bihar', status: 'preview' },
  { code: 'vjk', language: 'vjk-IN', iso639_3: 'vjk', englishName: 'Bajjika', nativeName: 'बज्जिका', direction: 'ltr', group: 'bihar', status: 'preview' },
  { code: 'mag', language: 'mag-IN', iso639_3: 'mag', englishName: 'Magahi', nativeName: 'मगही', direction: 'ltr', group: 'bihar', status: 'preview' },
] as const satisfies readonly UiLanguageDefinition[]

export type UiLocaleCode = typeof UI_LANGUAGES[number]['code']
export type UiLanguage = typeof UI_LANGUAGES[number]

export const UI_LOCALE_CODES = UI_LANGUAGES.map(language => language.code) as UiLocaleCode[]
export const INDIAN_LOCALE_CODES = UI_LANGUAGES
  .filter(language => language.group !== 'global')
  .map(language => language.code) as UiLocaleCode[]

export function findUiLanguage(code: string | null | undefined): UiLanguage | undefined {
  if (!code) return undefined
  const normalized = code.toLowerCase()
  return UI_LANGUAGES.find(language => (
    language.code.toLowerCase() === normalized
    || language.language.toLowerCase() === normalized
    || language.language.toLowerCase().split('-')[0] === normalized.split('-')[0]
  ))
}

export function groupUiLanguages(indianContext: boolean): Array<{
  key: UiLanguageGroup
  languages: readonly UiLanguage[]
}> {
  const order: UiLanguageGroup[] = indianContext
    ? ['indian', 'bihar', 'global']
    : ['global', 'indian', 'bihar']

  return order.map(key => ({
    key,
    languages: UI_LANGUAGES.filter(language => language.group === key),
  }))
}

export const NUXT_I18N_LOCALES = UI_LANGUAGES.map(language => ({
  code: language.code,
  name: language.nativeName,
  language: language.language,
  dir: language.direction,
  file: `${language.code}.json`,
}))
