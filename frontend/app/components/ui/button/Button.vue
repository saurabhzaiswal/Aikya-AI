<template>
  <component
    :is="tag"
    :class="classes"
    :disabled="tag === 'button' ? disabled : undefined"
  >
    <slot />
  </component>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import { cn } from '~/utils/cn'

export default defineComponent({
  name: 'UiButton',
  props: {
    tag: { type: String as PropType<'button' | 'span'>, default: 'button' },
    variant: { type: String as PropType<'primary' | 'secondary' | 'ghost'>, default: 'primary' },
    disabled: { type: Boolean, default: false },
    className: { type: String, default: '' },
  },
  computed: {
    classes(): string {
      return cn(
        this.variant === 'primary' && 'button-primary',
        this.variant === 'secondary' && 'button-secondary',
        this.variant === 'ghost' && 'inline-flex min-h-11 items-center justify-center rounded-xl px-4 font-bold text-muted hover:bg-subtle hover:text-ink',
        this.className,
      )
    },
  },
})
</script>
