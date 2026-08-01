<template>
  <details
    ref="details"
    data-language-switcher
    class="group relative"
  >
    <summary
      class="flex min-h-11 cursor-pointer list-none items-center gap-2 rounded-xl border border-border bg-surface px-3 text-sm font-black text-ink hover:bg-subtle focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand"
      :aria-label="$t('locale.current', { language: currentLanguage.nativeName })"
    >
      <Globe2
        :size="17"
        aria-hidden="true"
      />
      <span>{{ currentLanguage.nativeName }}</span>
      <ChevronDown
        class="transition-transform group-open:rotate-180"
        :size="16"
        aria-hidden="true"
      />
    </summary>
    <div class="fixed inset-x-4 top-20 z-50 max-h-[min(72vh,42rem)] overflow-y-auto rounded-2xl border border-border bg-surface p-3 shadow-2xl sm:absolute sm:inset-x-auto sm:right-0 sm:top-[calc(100%+0.5rem)] sm:w-[28rem]">
      <p class="px-2 pb-3 text-sm font-black text-ink">
        {{ $t('locale.selectorTitle') }}
      </p>
      <section
        v-for="group in groups"
        :key="group.key"
        class="border-t border-border py-3 first:border-t-0 first:pt-0"
      >
        <h2 class="px-2 pb-2 text-xs font-black uppercase tracking-[0.16em] text-muted">
          {{ $t(`locale.groups.${group.key}`) }}
        </h2>
        <div class="grid gap-1 sm:grid-cols-2">
          <button
            v-for="language in group.languages"
            :key="language.code"
            class="flex min-h-12 items-center gap-3 rounded-xl px-3 py-2 text-left hover:bg-subtle"
            :class="{ 'bg-brand/10 text-brand': currentLanguage.code === language.code }"
            type="button"
            :lang="language.language"
            :dir="language.direction"
            :aria-current="currentLanguage.code === language.code ? 'true' : undefined"
            @click="selectLanguage(language.code)"
          >
            <span class="min-w-0 flex-1">
              <span class="block truncate font-black">{{ language.nativeName }}</span>
              <span class="block truncate text-xs text-muted">{{ language.englishName }}</span>
            </span>
            <span
              v-if="language.status === 'preview'"
              class="rounded-full bg-warning/10 px-2 py-1 text-[0.65rem] font-black text-warning"
            >{{ $t('locale.preview') }}</span>
            <Check
              v-if="currentLanguage.code === language.code"
              :size="17"
              aria-hidden="true"
            />
          </button>
        </div>
      </section>
    </div>
  </details>
</template>

<script lang="ts">
import { Check, ChevronDown, Globe2 } from 'lucide-vue-next'
import { defineComponent } from 'vue'
import type { LanguageGroupView } from '~/composables/useLanguageDetection'
import type { UiLanguage, UiLocaleCode } from '~/i18n/language-registry'

export default defineComponent({
  name: 'LocaleSwitcher',
  components: { Check, ChevronDown, Globe2 },
  computed: {
    currentLanguage(): UiLanguage {
      return this.$languagePreference.currentLanguage.value
    },
    groups(): LanguageGroupView[] {
      return this.$languagePreference.groups.value
    },
  },
  methods: {
    async selectLanguage(code: UiLocaleCode): Promise<void> {
      await this.$languagePreference.selectLocale(code)
      const details = this.$refs.details as HTMLDetailsElement | undefined
      if (details) details.open = false
    },
  },
})
</script>
