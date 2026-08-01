<template>
  <div>
    <section class="page-shell py-16 sm:py-24">
      <div class="grid items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
        <div>
          <p class="eyebrow">
            Why Aikya exists
          </p>
          <h1 class="display-title mt-5">
            Language should open doors, not define limits.
          </h1>
          <p class="body-lead mt-6">
            Aikya AI is an independent SaaS project focused on helping people understand important text and documents across languages.
          </p>
        </div>
        <div class="panel p-7 sm:p-9">
          <p class="text-sm font-bold text-muted">
            Mission
          </p>
          <blockquote class="mt-4 text-3xl font-black leading-tight tracking-tight">
            “One World.<br><span class="text-brand">One Understanding.</span>”
          </blockquote>
        </div>
      </div>
    </section>
    <section class="border-y border-border bg-surface py-20">
      <div class="page-shell grid gap-12 lg:grid-cols-2">
        <div>
          <p class="eyebrow">
            Founder
          </p><h2 class="section-title mt-4">
            Built independently by Saurabh Choudhary.
          </h2>
        </div>
        <div class="space-y-5 leading-8 text-muted">
          <p>Saurabh is building Aikya AI as a solo founder with AI-assisted engineering. Product, architecture, brand, and business decisions remain founder-led.</p>
          <p>The project favors clear scope, long-term maintainability, user privacy, and honest product communication over premature complexity.</p>
          <div class="flex flex-wrap gap-3 pt-2">
            <a
              v-for="profile in profiles"
              :key="profile.label"
              class="button-secondary !min-h-11"
              :href="profile.href"
              rel="me noopener"
              target="_blank"
            >{{ profile.label }} <ExternalLink :size="15" /></a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ExternalLink } from 'lucide-vue-next'
import { FOUNDER } from '~/seo/constants'
import { PAGE_METADATA } from '~/seo/metadata'
import { breadcrumbSchema } from '~/seo/schemas'

const config = useRuntimeConfig()
usePageSeo({ ...PAGE_METADATA.about, schemas: [breadcrumbSchema(config.public.siteUrl, [{ name: 'Home', path: '/' }, { name: 'About', path: '/about' }])] })
const profiles = [
  { label: 'LinkedIn', href: FOUNDER.linkedIn },
  { label: 'GitHub', href: FOUNDER.github },
  { label: 'Dev Community', href: FOUNDER.dev },
  { label: 'Portfolio', href: FOUNDER.portfolio },
]
</script>
