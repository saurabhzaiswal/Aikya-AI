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
        Article not found
      </h1><NuxtLink
        class="text-link mt-5 inline-block"
        to="/blog"
      >Back to blog</NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
import { resolveContentSocialImage } from '~/seo/social-images'

const route = useRoute()
const { data: page } = await useAsyncData(`blog-${route.path}`, () => queryCollection('blog').path(route.path).first())
if (page.value) usePageSeo({ title: page.value.title, description: page.value.description, socialImage: resolveContentSocialImage(route.path, 'blog') })
else usePageSeo({ title: 'Article not found', description: 'The requested Aikya AI article was not found.', noIndex: true })
</script>
