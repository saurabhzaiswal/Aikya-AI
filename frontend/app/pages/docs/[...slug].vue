<template>
  <section class="page-shell py-16 sm:py-24">
    <ContentRenderer
      v-if="page"
      class="prose-aikya"
      :value="page"
    />
    <div
      v-else
      class="mx-auto max-w-xl text-center"
    >
      <h1 class="section-title">
        Guide not found
      </h1><NuxtLink
        class="text-link mt-5 inline-block"
        to="/docs"
      >Back to documentation</NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
const route = useRoute()
const { data: page } = await useAsyncData(`docs-${route.path}`, () => queryCollection('docs').path(route.path).first())
if (page.value) usePageSeo({ title: page.value.title, description: page.value.description, socialImage: 'knowledge' })
else usePageSeo({ title: 'Guide not found', description: 'The requested Aikya AI guide was not found.', noIndex: true })
</script>
