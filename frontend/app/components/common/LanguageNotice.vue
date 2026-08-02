<template>
  <aside
    v-if="notice"
    class="fixed bottom-4 left-1/2 z-50 flex w-[min(92vw,38rem)] -translate-x-1/2 items-center gap-3 rounded-2xl border border-border bg-surface p-4 shadow-2xl"
    role="status"
    aria-live="polite"
  >
    <Globe2
      class="shrink-0 text-brand"
      :size="20"
      aria-hidden="true"
    />
    <p class="min-w-0 flex-1 text-sm font-semibold text-ink">
      {{ message }}
    </p>
    <button
      class="ripple-control rounded-lg px-2 py-1 text-sm font-black text-brand hover:bg-subtle"
      type="button"
      @click="openSwitcher"
    >
      {{ $t('locale.change') }}
    </button>
    <button
      class="ripple-control grid size-9 shrink-0 place-items-center rounded-lg text-muted hover:bg-subtle hover:text-ink"
      type="button"
      :aria-label="$t('actions.dismiss')"
      @click="dismiss"
    >
      <X
        :size="18"
        aria-hidden="true"
      />
    </button>
  </aside>
</template>

<script lang="ts">
import { Globe2, X } from '@lucide/vue'
import { defineComponent } from 'vue'
import type { LanguageDetectionNotice } from '~/composables/useLanguageDetection'

export default defineComponent({
  name: 'LanguageNotice',
  components: { Globe2, X },
  computed: {
    notice(): LanguageDetectionNotice | null {
      return this.$languagePreference.notice.value
    },
    message(): string {
      if (!this.notice) return ''
      return this.notice.kind === 'detected'
        ? this.$t('locale.detected', { language: this.notice.languageName })
        : this.$t('locale.unsupported')
    },
  },
  methods: {
    openSwitcher(): void {
      const switchers = Array.from(
        document.querySelectorAll<HTMLDetailsElement>('details[data-language-switcher]'),
      )
      const switcher = switchers.find(element => element.offsetParent !== null) ?? switchers[0]
      if (!switcher) return
      switcher.open = true
      switcher.querySelector<HTMLElement>('summary')?.focus()
      this.dismiss()
    },
    dismiss(): void {
      this.$languagePreference.dismissNotice()
    },
  },
})
</script>
