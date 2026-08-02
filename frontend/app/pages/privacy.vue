<template>
  <section class="page-shell py-16 sm:py-24">
    <article class="prose-aikya">
      <p class="eyebrow">
        Legal draft
      </p>
      <h1>Privacy policy</h1>
      <div class="rounded-2xl border border-warning/30 bg-surface p-5 text-sm text-warning">
        <strong>Draft-not effective.</strong> This notice documents the intended Phase 1 privacy posture and requires legal review before public launch.
      </div>
      <h2>What the MVP processes</h2>
      <p>Account details, workspace identifiers, submitted text, uploaded digital PDF documents, translation output, security logs, and limited operational metadata may be processed to provide the service.</p>
      <h2>How content is handled</h2>
      <p>Text or document content may be sent to the translation provider configured by the operator. Optional AI providers are not invoked unless a future feature explicitly requires and discloses that use.</p>
      <h2>Retention and access</h2>
      <p>Phase 1 is designed for temporary document retention and workspace-scoped access. Exact production retention windows, deletion workflows, subprocessors, and data-rights contacts must be confirmed before launch.</p>
      <h2>Contact</h2>
      <p>Until a formal privacy address is published, use the verified founder profiles on the <NuxtLink to="/contact">contact page</NuxtLink>.</p>
    </article>
  </section>
</template>

<script setup lang="ts">
import { PAGE_METADATA } from '~/seo/metadata'

usePageSeo(PAGE_METADATA.privacy)
</script>
