<template>
  <NuxtLink
    class="group inline-flex items-center gap-3"
    :to="$localePath('/')"
    aria-label="Aikya AI home"
  >
    <span class="grid size-10 place-items-center transition-transform duration-200 group-hover:-rotate-2 group-hover:scale-[1.03]">
      <img
        :src="inverse ? '/brand/aikya-mark-dark.svg' : '/brand/aikya-mark.svg'"
        alt=""
        width="40"
        height="40"
        class="size-10"
      >
    </span>
    <span>
      <span class="block text-lg font-black leading-none tracking-[-0.035em]">Aikya</span>
      <span
        v-if="showTagline"
        class="mt-1 block text-[0.68rem] font-semibold"
        :class="inverse ? 'text-on-brand/70' : 'text-muted'"
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
    inverse: { type: Boolean, default: false },
  },
})
</script>
