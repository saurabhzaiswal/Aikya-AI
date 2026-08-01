<template>
  <div
    class="flex min-h-11 items-center gap-1 rounded-xl border border-border bg-surface p-1"
    role="group"
    :aria-label="$t('locale.label')"
  >
    <SwitchLocalePathLink
      v-for="item in locales"
      :key="item.code"
      :locale="item.code"
      :lang="item.language"
      class="rounded-lg px-2 py-1 text-xs font-black text-muted hover:text-ink"
      :class="{ 'bg-subtle text-ink': $i18n.locale === item.code }"
      :aria-current="$i18n.locale === item.code ? 'page' : undefined"
    >
      {{ item.shortLabel }}
    </SwitchLocalePathLink>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

type LocaleCode = 'en' | 'hi'

interface LocaleOption {
  code: LocaleCode
  language: string
  shortLabel: string
}

export default defineComponent({
  name: 'LocaleSwitcher',
  data(): { locales: LocaleOption[] } {
    return {
      locales: [
        { code: 'en', language: 'en-US', shortLabel: 'EN' },
        { code: 'hi', language: 'hi-IN', shortLabel: 'हिं' },
      ],
    }
  },
})
</script>
