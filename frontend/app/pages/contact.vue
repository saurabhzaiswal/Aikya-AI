<template>
  <section class="page-shell py-16 sm:py-24">
    <div class="mx-auto max-w-3xl text-center">
      <p class="eyebrow">
        Contact
      </p>
      <h1 class="display-title mt-5">
        Connect through verified public profiles.
      </h1>
      <p class="body-lead mt-6">
        A public support inbox is not active during Phase 1. For founder and project conversations, use one of the profiles below.
      </p>
    </div>
    <div class="mx-auto mt-12 grid max-w-4xl gap-5 sm:grid-cols-2">
      <a
        v-for="profile in profiles"
        :key="profile.label"
        class="panel group flex items-center justify-between p-6 hover:-translate-y-1 hover:border-brand/40"
        :href="profile.href"
        rel="me noopener"
        target="_blank"
      >
        <div><p class="text-xs font-bold uppercase tracking-widest text-muted">{{ profile.type }}</p><h2 class="mt-2 text-xl font-black">{{ profile.label }}</h2><p class="mt-1 text-sm text-muted">{{ profile.handle }}</p></div>
        <ExternalLink
          class="text-brand transition-transform group-hover:translate-x-1 group-hover:-translate-y-1"
          :size="20"
        />
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ExternalLink } from '@lucide/vue'
import { FOUNDER } from '~/seo/constants'
import { PAGE_METADATA } from '~/seo/metadata'

usePageSeo(PAGE_METADATA.contact)
const profiles = [
  { type: 'Professional profile', label: 'LinkedIn', handle: 'Saurabh Choudhary', href: FOUNDER.linkedIn },
  { type: 'Source profile', label: 'GitHub', handle: '@saurabhzaiswal', href: FOUNDER.github },
  { type: 'Writing', label: 'Dev Community', handle: '@saurabhzaiswal', href: FOUNDER.dev },
  { type: 'Personal site', label: 'Portfolio', handle: 'saurabhzaiswal.vercel.app', href: FOUNDER.portfolio },
]
</script>
