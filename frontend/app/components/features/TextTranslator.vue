<template>
  <section
    class="panel p-5 sm:p-7"
    aria-labelledby="text-translation-title"
  >
    <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
      <div>
        <p class="eyebrow">
          Text
        </p><h2
          id="text-translation-title"
          class="mt-2 text-2xl font-black tracking-tight"
        >
          Translate text
        </h2>
      </div>
      <span class="rounded-full bg-brand-soft px-3 py-1.5 text-xs font-bold text-brand">10,000 character limit</span>
    </div>
    <form
      class="space-y-4"
      @submit.prevent="translate"
    >
      <div class="grid gap-3 sm:grid-cols-2">
        <div>
          <label
            class="label"
            for="source-language"
          >From</label><select
            id="source-language"
            v-model="sourceLanguage"
            class="field"
          >
            <option value="auto">
              Detect automatically
            </option><option
              v-for="language in languages"
              :key="`source-${language.code}`"
              :value="language.code"
            >
              {{ language.name }}
            </option>
          </select>
        </div>
        <div>
          <label
            class="label"
            for="target-language"
          >To</label><select
            id="target-language"
            v-model="targetLanguage"
            class="field"
          >
            <option
              v-for="language in languages"
              :key="`target-${language.code}`"
              :value="language.code"
            >
              {{ language.name }}
            </option>
          </select>
        </div>
      </div>
      <div>
        <label
          class="label"
          for="source-text"
        >Source text</label><textarea
          id="source-text"
          v-model="sourceText"
          class="field min-h-44 resize-y py-3"
          maxlength="10000"
          placeholder="Enter the text you want to understand…"
          required
        /><p class="mt-1.5 text-right text-xs font-semibold text-muted">
          {{ sourceText.length.toLocaleString() }} / 10,000
        </p>
      </div>
      <p
        v-if="error"
        class="rounded-xl bg-danger/10 p-3 text-sm text-danger"
        role="alert"
      >
        {{ error }}
      </p>
      <button
        class="button-primary"
        type="submit"
        :disabled="loading || !sourceText.trim()"
      >
        {{ loading ? 'Translating…' : 'Translate text' }}
      </button>
    </form>
    <div
      v-if="result"
      class="mt-7 border-t border-border pt-6"
      aria-live="polite"
    >
      <div class="mb-3 flex items-center justify-between gap-3">
        <h3 class="font-black">
          Translation
        </h3><button
          class="text-link text-sm"
          type="button"
          @click="copyResult"
        >
          {{ copied ? 'Copied' : 'Copy' }}
        </button>
      </div>
      <p
        class="whitespace-pre-wrap rounded-2xl bg-canvas p-4 leading-7"
        :dir="resultDirection"
      >
        {{ result.translated_text }}
      </p>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { ApiError } from '~/services/api'
import type { Language, TextTranslation } from '~/types/api'

export default defineComponent({
  name: 'TextTranslator',
  props: { languages: { type: Array as PropType<Language[]>, required: true } },
  emits: ['translated'],
  data() {
    return { sourceLanguage: 'auto', targetLanguage: 'hi', sourceText: '', result: null as TextTranslation | null, loading: false, copied: false, error: '' }
  },
  computed: {
    resultDirection(): string {
      return this.languages.find(language => language.code === this.result?.target_language)?.direction || 'ltr'
    },
  },
  methods: {
    async translate(): Promise<void> {
      this.loading = true
      this.error = ''
      this.copied = false
      try {
        this.result = await this.$services.translation.translateText(this.sourceText, this.sourceLanguage, this.targetLanguage)
        this.$emit('translated', this.result)
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'Translation could not be completed.'
      }
      finally {
        this.loading = false
      }
    },
    async copyResult(): Promise<void> {
      if (!this.result) return
      await navigator.clipboard.writeText(this.result.translated_text)
      this.copied = true
    },
  },
})
</script>
