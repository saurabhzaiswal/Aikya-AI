<template>
  <div class="overflow-hidden">
    <section class="relative pb-20 pt-16 sm:pb-28 sm:pt-24">
      <div
        class="site-grid pointer-events-none absolute inset-0"
        aria-hidden="true"
      />
      <div
        class="absolute left-1/2 top-0 size-[36rem] -translate-x-1/2 rounded-full bg-brand/10 blur-3xl"
        aria-hidden="true"
      />
      <div class="page-shell relative text-center">
        <div class="mx-auto inline-flex items-center gap-2 rounded-full border border-brand/20 bg-brand-soft px-4 py-2 text-xs font-bold text-brand">
          <Sparkles
            :size="14"
            aria-hidden="true"
          />
          Focused Phase 1 MVP
        </div>
        <h1 class="display-title mx-auto mt-7 max-w-5xl">
          Understand what matters, <span class="text-brand">in your language.</span>
        </h1>
        <p class="body-lead mx-auto mt-7 max-w-3xl">
          Aikya AI gives you one calm, private workspace for translating text and creating readable translations of digital PDF documents.
        </p>
        <div class="mt-9 flex flex-col justify-center gap-3 sm:flex-row">
          <NuxtLink
            class="button-primary"
            :to="$localePath('/register')"
          >Create your workspace <ArrowRight
            :size="18"
            aria-hidden="true"
          /></NuxtLink>
          <NuxtLink
            class="button-secondary"
            to="/features"
          >Explore Phase 1 features</NuxtLink>
        </div>
        <div class="mt-7 flex flex-wrap justify-center gap-x-6 gap-y-2 text-xs font-semibold text-muted">
          <span class="inline-flex items-center gap-2"><ShieldCheck
            :size="15"
            class="text-accent"
          />Privacy-first defaults</span>
          <span class="inline-flex items-center gap-2"><ScanText
            :size="15"
            class="text-accent"
          />Text and digital PDFs</span>
          <span class="inline-flex items-center gap-2"><CircleGauge
            :size="15"
            class="text-accent"
          />Focused, honest MVP scope</span>
        </div>
      </div>
    </section>

    <section class="page-shell pb-24">
      <ProductPreview />
    </section>

    <section class="border-y border-border bg-surface py-20 sm:py-28">
      <div class="page-shell">
        <div class="max-w-2xl">
          <p class="eyebrow">
            One focused workspace
          </p>
          <h2 class="section-title mt-4">
            Built for understanding-not feature noise.
          </h2>
          <p class="body-lead mt-5">
            Phase 1 concentrates on the two workflows that prove the product: text translation and readable digital PDF translation.
          </p>
        </div>
        <div class="mt-12 grid gap-5 md:grid-cols-3">
          <FeatureCard
            :icon="Languages"
            title="Translate text"
            description="Detect a source language or choose one, translate up to 10,000 characters, and copy the result."
            note="Translation quality depends on the configured provider."
          />
          <FeatureCard
            :icon="FileText"
            title="Translate digital PDFs"
            description="Upload a supported text-based PDF, track the processing job, and download a readable translated PDF."
            note="Scanned-document OCR and layout fidelity are outside Phase 1."
          />
          <FeatureCard
            :icon="LockKeyhole"
            title="Privacy-aware by design"
            description="Short-lived access tokens, protected refresh cookies, workspace isolation, and temporary document retention form the baseline."
            note="Provider processing is disclosed before document upload."
          />
        </div>
      </div>
    </section>

    <section class="page-shell py-20 sm:py-28">
      <div class="grid items-center gap-12 lg:grid-cols-2">
        <div>
          <p class="eyebrow">
            Clear boundaries
          </p>
          <h2 class="section-title mt-4">
            Trust starts with saying what the product does today.
          </h2>
          <p class="body-lead mt-5">
            Aikya AI does not quietly invoke optional AI features, claim perfect document fidelity, or pretend an early MVP is a finished enterprise suite.
          </p>
          <NuxtLink
            class="text-link mt-7 inline-flex items-center gap-2"
            to="/features"
          >Read the feature boundaries <ArrowRight :size="16" /></NuxtLink>
        </div>
        <div class="panel divide-y divide-border overflow-hidden">
          <div
            v-for="item in trustItems"
            :key="item.title"
            class="flex gap-4 p-5 sm:p-6"
          >
            <CheckCircle2
              :size="21"
              class="mt-0.5 shrink-0 text-accent"
              aria-hidden="true"
            />
            <div>
              <h3 class="font-black">
                {{ item.title }}
              </h3><p class="mt-1 text-sm leading-6 text-muted">
                {{ item.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="page-shell pb-20 sm:pb-28">
      <div class="relative overflow-hidden rounded-[2rem] bg-brand px-6 py-14 text-center text-on-brand shadow-[0_1.5rem_4rem_rgb(79_70_229/0.24)] sm:px-12 sm:py-20">
        <div
          class="absolute inset-0 opacity-20 site-grid"
          aria-hidden="true"
        />
        <div class="relative mx-auto max-w-2xl">
          <p class="text-xs font-black uppercase tracking-[0.2em]">
            One World. One Understanding.
          </p>
          <h2 class="mt-4 text-3xl font-black tracking-tight sm:text-5xl">
            Start with a workspace that respects the scope.
          </h2>
          <p class="mx-auto mt-5 max-w-xl leading-7 opacity-85">
            Create an account and try the focused Phase 1 translation experience.
          </p>
          <NuxtLink
            class="mt-8 inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-on-brand px-5 font-black text-brand-strong hover:-translate-y-0.5"
            :to="$localePath('/register')"
          >Create your workspace <ArrowRight :size="18" /></NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ArrowRight, CheckCircle2, CircleGauge, FileText, Languages, LockKeyhole, ScanText, ShieldCheck, Sparkles } from '@lucide/vue'

import { PAGE_METADATA } from '~/seo/metadata'
import { organizationSchema, softwareSchema, websiteSchema } from '~/seo/schemas'

const config = useRuntimeConfig()
usePageSeo({
  ...PAGE_METADATA.home,
  path: '/',
  schemas: [
    organizationSchema(config.public.siteUrl),
    websiteSchema(config.public.siteUrl),
    softwareSchema(config.public.siteUrl),
  ],
})

const trustItems = [
  { title: 'Your account has a real workspace boundary', description: 'Phase 1 data access is scoped through organization and workspace context in the backend.' },
  { title: 'Document limits are visible before upload', description: 'The UI states accepted type, size, page, provider, and output limitations before work begins.' },
  { title: 'AI extras are not used silently', description: 'Optional summarization, rewriting, voice, billing, mobile, and desktop features are not part of this release.' },
]
</script>
