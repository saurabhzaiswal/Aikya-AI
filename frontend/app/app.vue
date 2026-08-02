<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLoadingIndicator color="var(--color-brand)" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <LanguageNotice />
    <ToastViewport />
  </div>
</template>

<script setup lang="ts">
import type { ReactiveHead } from '@unhead/vue'

defineOptions({ name: 'AikyaApp' })

const localeHead = useLocaleHead({ seo: true })
// Nuxt i18n and Unhead model the same head records through distinct public types.
useHead(() => localeHead.value as unknown as ReactiveHead)
</script>
