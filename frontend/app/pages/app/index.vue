<template>
  <div />
</template>

<script setup lang="ts">
definePageMeta({ layout: 'app', middleware: 'auth' })
usePageSeo({ title: 'Workspace', description: 'Aikya AI private workspace.', noIndex: true })
const localePath = useLocalePath()
await navigateTo(localePath('/app/dashboard'), { redirectCode: 302 })
</script>
