<template>
  <div>
    <section class="page-shell py-16 text-center sm:py-24">
      <p class="eyebrow">
        Phase 1 capabilities
      </p>
      <h1 class="display-title mx-auto mt-5 max-w-4xl">
        A clear path from content to understanding.
      </h1>
      <p class="body-lead mx-auto mt-6 max-w-2xl">
        The MVP is deliberately narrow: translate text, translate supported digital PDFs, and review recent workspace activity.
      </p>
    </section>
    <section class="page-shell pb-24">
      <div class="grid gap-6 lg:grid-cols-2">
        <article
          v-for="feature in features"
          :key="feature.title"
          class="panel p-6 sm:p-8"
        >
          <component
            :is="feature.icon"
            :size="24"
            class="text-brand"
            aria-hidden="true"
          />
          <h2 class="mt-5 text-2xl font-black tracking-tight">
            {{ feature.title }}
          </h2>
          <p class="mt-3 leading-7 text-muted">
            {{ feature.description }}
          </p>
          <ul class="mt-6 space-y-3">
            <li
              v-for="point in feature.points"
              :key="point"
              class="flex gap-3 text-sm leading-6"
            >
              <Check
                :size="17"
                class="mt-1 shrink-0 text-accent"
              />{{ point }}
            </li>
          </ul>
          <p class="mt-6 rounded-2xl bg-canvas p-4 text-xs font-semibold leading-5 text-muted">
            Boundary: {{ feature.boundary }}
          </p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Activity, Check, FileText, Languages, ShieldCheck } from '@lucide/vue'
import { PAGE_METADATA } from '~/seo/metadata'
import { breadcrumbSchema } from '~/seo/schemas'

const config = useRuntimeConfig()
usePageSeo({ ...PAGE_METADATA.features, schemas: [breadcrumbSchema(config.public.siteUrl, [{ name: 'Home', path: '/' }, { name: 'Features', path: '/features' }])] })

const features = [
  { icon: Languages, title: 'Text translation', description: 'A distraction-free translator for short-form content.', points: ['Automatic source-language detection', 'Explicit source and target language controls', 'Copy-ready translated result', 'Workspace translation history'], boundary: 'Up to 10,000 characters per request; quality depends on the configured provider.' },
  { icon: FileText, title: 'Digital PDF translation', description: 'A transparent upload-and-process flow for text-based PDF documents.', points: ['PDF validation and checksum', 'Malware-scanning workflow', 'Live job stage and progress', 'Short-lived download link'], boundary: 'Scanned PDFs need future OCR; Phase 1 produces a readable export without original-layout fidelity.' },
  { icon: Activity, title: 'Workspace activity', description: 'A simple dashboard for the work that matters now.', points: ['Recent documents', 'Recent text translations', 'Processing status', 'Manual refresh'], boundary: 'Advanced folders, search, analytics, team collaboration, and exports are not included yet.' },
  { icon: ShieldCheck, title: 'Security baseline', description: 'The MVP starts from explicit identity and privacy boundaries.', points: ['In-memory browser access token', 'Protected refresh-cookie flow', 'Organization and workspace context', 'Temporary document retention'], boundary: 'A formal production security review remains required before a public launch.' },
]
</script>
