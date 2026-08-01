<template>
  <DashboardWorkspace />
</template>

<script setup lang="ts">
defineI18nRoute(false)
definePageMeta({ layout: 'app', middleware: 'auth' })
usePageSeo({ title: 'Translation workspace', description: 'Translate text and supported PDF documents in your private Aikya AI workspace.', noIndex: true })
</script>
