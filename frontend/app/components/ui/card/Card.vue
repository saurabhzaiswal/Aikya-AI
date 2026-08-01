<template>
  <article :class="['panel', paddingClass]">
    <slot />
  </article>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export default defineComponent({
  name: 'UiCard',
  props: {
    padding: { type: String as PropType<'none' | 'small' | 'default'>, default: 'default' },
  },
  computed: {
    paddingClass(): string {
      return { none: '', small: 'p-5', default: 'p-6 sm:p-8' }[this.padding]
    },
  },
})
</script>
