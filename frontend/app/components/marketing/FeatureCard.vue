<template>
  <article class="group rounded-3xl border border-border bg-surface p-6 transition-transform hover:-translate-y-1 hover:border-brand/35 sm:p-7">
    <span class="grid size-12 place-items-center rounded-2xl bg-brand-soft text-brand">
      <component
        :is="icon"
        :size="22"
        aria-hidden="true"
      />
    </span>
    <h3 class="mt-5 text-xl font-black tracking-tight">
      {{ title }}
    </h3>
    <p class="mt-2 leading-7 text-muted">
      {{ description }}
    </p>
    <p
      v-if="note"
      class="mt-5 border-t border-border pt-4 text-xs font-semibold text-muted"
    >
      {{ note }}
    </p>
  </article>
</template>

<script lang="ts">
import { defineComponent, type Component, type PropType } from 'vue'

export default defineComponent({
  name: 'FeatureCard',
  props: {
    icon: { type: Object as PropType<Component>, required: true },
    title: { type: String, required: true },
    description: { type: String, required: true },
    note: { type: String, default: '' },
  },
})
</script>
