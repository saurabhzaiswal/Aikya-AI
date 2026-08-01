<template>
  <LoginForm />
</template>

<script setup lang="ts">
defineI18nRoute(false)
definePageMeta({ layout: 'auth', middleware: 'guest' })
usePageSeo({ title: 'Sign in', description: 'Sign in to your private Aikya AI workspace.', noIndex: true })
</script>
