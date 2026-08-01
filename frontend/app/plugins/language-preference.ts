export default defineNuxtPlugin({
  name: 'aikya-language-preference',
  setup() {
    return {
      provide: {
        languagePreference: useLanguageDetection(),
      },
    }
  },
})
