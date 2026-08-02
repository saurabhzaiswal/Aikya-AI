<template>
  <RegisterForm />
</template>

<script setup lang="ts">
// Auth pages stay directly reachable. Access control remains on private routes.
definePageMeta({ layout: 'auth' })
usePageSeo({ title: 'Create a workspace', description: 'Create an Aikya AI Phase 1 translation workspace.', noIndex: true })
</script>
