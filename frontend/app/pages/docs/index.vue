<template>
  <section class="page-shell py-16 sm:py-24">
    <div class="max-w-3xl">
      <p class="eyebrow">
        Documentation
      </p><h1 class="display-title mt-5">
        Use the Phase 1 workspace with confidence.
      </h1><p class="body-lead mt-6">
        Short, honest guides for the capabilities available today.
      </p>
    </div>
    <div class="mt-12 grid gap-5 md:grid-cols-2">
      <NuxtLink
        v-for="item in pages"
        :key="item.path"
        class="panel group p-6 hover:-translate-y-1 hover:border-brand/40 sm:p-8"
        :to="item.path"
      >
        <BookOpen
          :size="22"
          class="text-brand"
        /><h2 class="mt-5 text-2xl font-black group-hover:text-brand">{{ item.title }}</h2><p class="mt-3 leading-7 text-muted">{{ item.description }}</p>
      </NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import { BookOpen } from '@lucide/vue'

const { data: pages } = await useAsyncData('docs-list', () => queryCollection('docs').all())
usePageSeo({ title: 'Documentation', description: 'User documentation for the Aikya AI Phase 1 translation workspace.' })
</script>
