<template>
  <div class="min-h-screen bg-canvas text-ink">
    <a
      href="#main-content"
      class="sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:not-sr-only focus:rounded-xl focus:bg-surface focus:px-4 focus:py-3"
    >{{ $t('accessibility.skipToContent') }}</a>
    <SiteHeader />
    <main id="main-content">
      <slot />
    </main>
    <SiteFooter />
  </div>
</template>

<script lang="ts">
export default defineNuxtComponent({ name: 'DefaultLayout' })
</script>
