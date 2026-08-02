<template>
  <aside
    v-if="toasts.length"
    class="pointer-events-none fixed inset-x-4 top-4 z-[100] flex flex-col items-end gap-3 sm:inset-x-auto sm:right-5 sm:w-[24rem]"
    :aria-label="$t('toast.notifications')"
  >
    <article
      v-for="toast in toasts"
      :key="toast.id"
      class="pointer-events-auto flex w-full items-start gap-3 rounded-2xl border border-border bg-surface/95 p-4 text-ink shadow-2xl backdrop-blur-xl"
      :class="accentClass(toast.kind)"
      :role="toast.kind === 'error' ? 'alert' : 'status'"
    >
      <CircleAlert
        v-if="toast.kind === 'error'"
        class="mt-0.5 shrink-0 text-danger"
        :size="20"
        aria-hidden="true"
      />
      <CircleCheck
        v-else-if="toast.kind === 'success'"
        class="mt-0.5 shrink-0 text-success"
        :size="20"
        aria-hidden="true"
      />
      <Info
        v-else
        class="mt-0.5 shrink-0 text-brand"
        :size="20"
        aria-hidden="true"
      />
      <p class="min-w-0 flex-1 text-sm font-semibold leading-6">
        {{ toast.message }}
      </p>
      <button
        class="ripple-control grid size-8 shrink-0 place-items-center rounded-lg text-muted hover:bg-subtle hover:text-ink"
        type="button"
        :aria-label="$t('actions.dismiss')"
        @click="dismiss(toast.id)"
      >
        <X
          :size="17"
          aria-hidden="true"
        />
      </button>
    </article>
  </aside>
</template>

<script lang="ts">
import { CircleAlert, CircleCheck, Info, X } from '@lucide/vue'
import { defineComponent } from 'vue'
import { useToastStore, type ToastKind, type ToastMessage } from '~/stores/toast'

export default defineComponent({
  name: 'ToastViewport',
  components: { CircleAlert, CircleCheck, Info, X },
  computed: {
    toasts(): ToastMessage[] {
      return useToastStore().items
    },
  },
  methods: {
    accentClass(kind: ToastKind): string {
      return {
        error: 'border-l-4 border-l-danger',
        success: 'border-l-4 border-l-success',
        info: 'border-l-4 border-l-brand',
      }[kind]
    },
    dismiss(id: number): void {
      useToastStore().dismiss(id)
    },
  },
})
</script>
