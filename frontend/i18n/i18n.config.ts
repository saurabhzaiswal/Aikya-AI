export default defineI18nConfig(() => ({
  legacy: false,
  locale: 'en',
  fallbackLocale: {
    bho: ['hi', 'en'],
    mai: ['hi', 'en'],
    vjk: ['hi', 'en'],
    mag: ['hi', 'en'],
    default: ['en'],
  },
  missingWarn: true,
  fallbackWarn: true,
}))
