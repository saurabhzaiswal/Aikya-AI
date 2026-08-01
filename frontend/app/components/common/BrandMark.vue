<template>
  <NuxtLink
    class="group inline-flex items-center gap-3"
    to="/"
    aria-label="Aikya AI home"
  >
    <span class="grid size-10 place-items-center rounded-[0.9rem] bg-brand text-lg font-black text-on-brand shadow-[0_0.7rem_1.5rem_rgb(79_70_229/0.22)] transition-transform group-hover:-rotate-3">
      A
    </span>
    <span>
      <span class="block text-base font-black leading-none tracking-tight">Aikya AI</span>
      <span
        v-if="showTagline"
        class="mt-1 block text-[0.68rem] font-semibold text-muted"
      >One World. One Understanding.</span>
    </span>
  </NuxtLink>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'BrandMark',
  props: {
    showTagline: { type: Boolean, default: true },
  },
})
</script>
