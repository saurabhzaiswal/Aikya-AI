<template>
  <section class="page-shell py-16 sm:py-24">
    <div class="max-w-3xl">
      <p class="eyebrow">
        Founder notes
      </p><h1 class="display-title mt-5">
        Building in public, with clear boundaries.
      </h1><p class="body-lead mt-6">
        Product thinking, architecture choices, and lessons from building Aikya AI as a solo founder.
      </p>
    </div>
    <div class="mt-12 grid gap-5 md:grid-cols-2">
      <NuxtLink
        v-for="article in articles"
        :key="article.path"
        class="panel group p-6 hover:-translate-y-1 hover:border-brand/40 sm:p-8"
        :to="article.path"
      >
        <p class="text-xs font-bold uppercase tracking-widest text-muted">{{ formatDate(article.date) }}</p>
        <h2 class="mt-4 text-2xl font-black tracking-tight group-hover:text-brand">{{ article.title }}</h2>
        <p class="mt-3 leading-7 text-muted">{{ article.description }}</p>
        <span class="text-link mt-6 inline-flex">Read article →</span>
      </NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
const { data: articles } = await useAsyncData('blog-list', () => queryCollection('blog').order('date', 'DESC').all())
usePageSeo({ title: 'Blog', description: 'Product and engineering notes from the Aikya AI founder.', socialImage: 'blog' })
function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(new Date(value))
}
</script>
