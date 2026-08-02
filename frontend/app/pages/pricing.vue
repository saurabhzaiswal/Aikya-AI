<template>
  <section class="page-shell py-16 sm:py-24">
    <div class="mx-auto max-w-3xl text-center">
      <p class="eyebrow">
        Pricing
      </p>
      <h1 class="display-title mt-5">
        Validate value before adding billing.
      </h1>
      <p class="body-lead mt-6">
        Aikya AI is currently a Phase 1 MVP. Public plans, payment collection, and paid subscriptions are not active.
      </p>
    </div>
    <div class="panel mx-auto mt-12 max-w-2xl p-7 sm:p-10">
      <div class="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="eyebrow">
            Private MVP
          </p><h2 class="mt-3 text-3xl font-black">
            Early access
          </h2><p class="mt-2 text-muted">
            Founder-led product validation
          </p>
        </div>
        <span class="rounded-full bg-brand-soft px-4 py-2 text-sm font-black text-brand">No public price yet</span>
      </div>
      <ul class="mt-8 grid gap-4 sm:grid-cols-2">
        <li
          v-for="item in included"
          :key="item"
          class="flex gap-3 text-sm"
        >
          <CheckCircle2
            :size="18"
            class="shrink-0 text-accent"
          />{{ item }}
        </li>
      </ul>
      <div class="mt-8 rounded-2xl bg-canvas p-5 text-sm leading-6 text-muted">
        Pricing will only be published after usage costs, privacy obligations, and customer value have been validated. No checkout or billing data is collected in Phase 1.
      </div>
      <NuxtLink
        class="button-primary mt-8 w-full"
        :to="$localePath('/register')"
      >Request MVP access</NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import { CheckCircle2 } from '@lucide/vue'
import { PAGE_METADATA } from '~/seo/metadata'
import { faqSchema } from '~/seo/schemas'

const faq = [
  { question: 'Is Aikya AI charging users in Phase 1?', answer: 'No. Public plans and payment collection are not active in the Phase 1 MVP.' },
  { question: 'When will pricing be announced?', answer: 'Pricing will be published only after product value and operating costs have been validated.' },
]
usePageSeo({ ...PAGE_METADATA.pricing, schemas: [faqSchema(faq)] })
const included = ['Text translation', 'Digital PDF translation', 'Recent workspace activity', 'Privacy-aware session design']
</script>
