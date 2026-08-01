<template>
  <div />
</template>

<script setup lang="ts">
defineI18nRoute(false)
definePageMeta({ layout: 'app', middleware: 'auth' })
usePageSeo({ title: 'Workspace', description: 'Aikya AI private workspace.', noIndex: true })
await navigateTo('/app/dashboard', { redirectCode: 302 })
</script>
