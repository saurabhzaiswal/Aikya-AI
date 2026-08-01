<template>
  <section class="page-shell py-16 sm:py-24">
    <article class="prose-aikya">
      <p class="eyebrow">
        Legal draft
      </p>
      <h1>Terms of service</h1>
      <div class="rounded-2xl border border-warning/30 bg-surface p-5 text-sm text-warning">
        <strong>Draft—not effective.</strong> These terms are a product-planning draft and require legal review before public availability.
      </div>
      <h2>Phase 1 service</h2>
      <p>Aikya AI currently provides a limited MVP for text and supported digital PDF translation. Availability, language support, output quality, and processing time are not guaranteed.</p>
      <h2>Acceptable use</h2>
      <p>Users must only submit content they are permitted to process and must not use the service for unlawful, abusive, harmful, or rights-infringing activity.</p>
      <h2>Translation limitations</h2>
      <p>Machine-generated translations may contain errors and must not be treated as professional legal, medical, financial, or certified translation advice.</p>
      <h2>Ownership</h2>
      <p>Aikya AI software is proprietary and owned by Saurabh Choudhary. Users retain responsibility for the content they submit.</p>
      <h2>Contact</h2>
      <p>Use the verified public channels on the <NuxtLink to="/contact">contact page</NuxtLink> until formal service contacts are published.</p>
    </article>
  </section>
</template>

<script setup lang="ts">
import { PAGE_METADATA } from '~/seo/metadata'

usePageSeo(PAGE_METADATA.terms)
</script>
