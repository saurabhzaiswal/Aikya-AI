import tailwindcss from '@tailwindcss/vite'
import { NUXT_I18N_LOCALES } from './app/i18n/language-registry'

const publicSiteUrl = process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000'
const apiProxyOrigin = process.env.NUXT_API_PROXY_TARGET || 'http://localhost:8000'
const apiProxyTarget = new URL('/api', apiProxyOrigin).toString()
const publicSiteHostname = new URL(publicSiteUrl).hostname
const siteEnvironment = process.env.AIKYA_ENV
  || (['localhost', '127.0.0.1', '::1'].includes(publicSiteHostname)
    ? 'development'
    : process.env.NODE_ENV || 'production')
const modules = [
  '@pinia/nuxt',
  '@vueuse/nuxt',
  'nuxt-site-config',
  '@nuxtjs/robots',
  '@nuxtjs/sitemap',
  '@nuxt/content',
  '@nuxtjs/i18n',
  'shadcn-nuxt',
  'reka-ui/nuxt',
  '@nuxt/eslint',
]

export default defineNuxtConfig({
  modules,
  ssr: true,
  components: [
    { path: '~/components/common', pathPrefix: false },
    { path: '~/components/features', pathPrefix: false },
    { path: '~/components/layout', pathPrefix: false },
    { path: '~/components/marketing', pathPrefix: false },
  ],
  devtools: { enabled: false },
  app: {
    head: {
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'theme-color', content: '#4338ca' },
      ],
      link: [{ rel: 'icon', href: '/favicon.svg', type: 'image/svg+xml' }],
    },
  },
  css: ['~/assets/styles/main.scss', '~/assets/styles/tailwind.css'],
  site: {
    url: publicSiteUrl,
    env: siteEnvironment,
    name: 'Aikya AI',
    description: 'Privacy-focused text and digital document translation.',
    defaultLocale: 'en',
  },
  content: {
    database: { type: 'sqlite', filename: ':memory:' },
    experimental: { sqliteConnector: 'native' },
  },
  runtimeConfig: {
    public: {
      siteUrl: publicSiteUrl,
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
    },
  },
  routeRules: {
    '/': { prerender: true },
    '/features': { prerender: true },
    '/about': { prerender: true },
    '/contact': { prerender: true },
    '/pricing': { prerender: true },
    '/privacy': { prerender: true },
    '/terms': { prerender: true },
    '/app/**': { ssr: false },
    '/**/app/**': { ssr: false },
    '/login': { ssr: false },
    '/register': { ssr: false },
    '/**/login': { ssr: false },
    '/**/register': { ssr: false },
    '/signup': { redirect: '/register' },
  },
  compatibilityDate: '2026-08-01',
  nitro: {
    devProxy: {
      '/api': {
        // Nitro removes the mounted /api prefix before forwarding.
        target: apiProxyTarget,
        changeOrigin: true,
      },
    },
    prerender: {
      crawlLinks: true,
      routes: ['/', '/features', '/about', '/contact', '/pricing', '/privacy', '/terms'],
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  eslint: {
    config: { stylistic: true },
  },
  i18n: {
    baseUrl: publicSiteUrl,
    defaultLocale: 'en',
    defaultDirection: 'ltr',
    strategy: 'prefix_except_default',
    locales: NUXT_I18N_LOCALES,
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'aikya_locale',
      redirectOn: 'root',
      fallbackLocale: 'en',
    },
    vueI18n: './i18n.config.ts',
    experimental: {
      prerenderMessages: true,
    },
  },
  pinia: {
    storesDirs: ['app/stores/**'],
  },
  robots: {
    disallow: ['/app', '/app/**', '/*/app', '/*/app/**', '/login', '/register', '/signup', '/*/login', '/*/register'],
  },
  shadcn: {
    // Barrel exports already use the Ui prefix (for example, UiCard).
    prefix: '',
    componentDir: './app/components/ui',
  },
  sitemap: {
    exclude: ['/app/**', '/*/app/**', '/login', '/register', '/signup', '/*/login', '/*/register'],
    zeroRuntime: true,
  },
})
