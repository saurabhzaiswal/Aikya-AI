<template>
  <LoginForm />
</template>

<script setup lang="ts">
// Auth pages stay directly reachable. Access control remains on private routes.
definePageMeta({ layout: 'auth' })
usePageSeo({ title: 'Sign in', description: 'Sign in to your private Aikya AI workspace.', noIndex: true })
</script>
