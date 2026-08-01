import type { ApiClient } from './api'
import type { Language, TextTranslation } from '~/types/api'

export class TranslationService {
  constructor(private readonly api: ApiClient) {}

  listLanguages(): Promise<Language[]> {
    return this.api.request({ method: 'GET', url: '/api/v1/translation/languages' })
  }

  translateText(text: string, sourceLanguage: string, targetLanguage: string): Promise<TextTranslation> {
    return this.api.request({
      method: 'POST',
      url: '/api/v1/translation/text',
      data: { text, source_language: sourceLanguage, target_language: targetLanguage },
    })
  }
}
