<template>
  <RegisterForm />
</template>

<script setup lang="ts">
defineI18nRoute(false)
definePageMeta({ layout: 'auth', middleware: 'guest' })
usePageSeo({ title: 'Create a workspace', description: 'Create an Aikya AI Phase 1 translation workspace.', noIndex: true })
</script>
