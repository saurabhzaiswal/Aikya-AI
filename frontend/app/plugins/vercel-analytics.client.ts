export default defineNuxtPlugin(() => {
  if (import.meta.dev) return

  if (document.querySelector('script[data-vpe-vercel-analytics]')) {
    return
  }

  const script = document.createElement('script')

  script.defer = true
  script.src = '/_vercel/insights/script.js'
  script.dataset.vpeVercelAnalytics = 'true'

  document.head.appendChild(script)
})