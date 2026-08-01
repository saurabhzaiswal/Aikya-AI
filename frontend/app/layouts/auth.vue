<template>
  <div class="relative grid min-h-screen place-items-center overflow-hidden bg-canvas px-4 py-10 text-ink">
    <div
      class="site-grid pointer-events-none absolute inset-0"
      aria-hidden="true"
    />
    <div
      class="absolute left-[8%] top-[12%] size-72 rounded-full bg-brand/10 blur-3xl"
      aria-hidden="true"
    />
    <div class="relative z-10 w-full max-w-md">
      <div class="mb-7 flex justify-center">
        <BrandMark />
      </div>
      <div class="mb-4 flex justify-center">
        <LocaleSwitcher />
      </div>
      <slot />
      <p class="mt-6 text-center text-xs text-muted">
        <NuxtLinkLocale
          class="hover:text-ink"
          to="/"
        >
          ← Aikya AI
        </NuxtLinkLocale>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
export default defineNuxtComponent({ name: 'AuthLayout' })
</script>
