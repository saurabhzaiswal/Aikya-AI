<template>
  <section
    class="panel p-5 sm:p-7"
    aria-labelledby="pdf-translation-title"
  >
    <div class="mb-6">
      <p class="eyebrow !text-accent">
        PDF
      </p><h2
        id="pdf-translation-title"
        class="mt-2 text-2xl font-black tracking-tight"
      >
        Translate a digital PDF
      </h2><p class="mt-2 text-sm leading-6 text-muted">
        Phase 1 extracts embedded text and creates a readable translated PDF. Scanned documents require future OCR.
      </p>
    </div>
    <form
      class="space-y-4"
      @submit.prevent="start"
    >
      <div>
        <label
          class="label"
          for="pdf-file"
        >PDF file</label><input
          id="pdf-file"
          class="field py-2 file:mr-3 file:rounded-lg file:border-0 file:bg-brand-soft file:px-3 file:py-2 file:font-bold file:text-brand"
          type="file"
          accept="application/pdf,.pdf"
          required
          @change="selectFile"
        >
      </div>
      <div>
        <label
          class="label"
          for="pdf-target-language"
        >Translate to</label><select
          id="pdf-target-language"
          v-model="targetLanguage"
          class="field"
        >
          <option
            v-for="language in languages"
            :key="language.code"
            :value="language.code"
          >
            {{ language.name }}
          </option>
        </select>
      </div>
      <div class="rounded-2xl border border-border bg-canvas p-4 text-sm leading-6 text-muted">
        <p>Maximum 50 MB and 100 pages. Temporary retention is the intended default.</p><p class="mt-1">
          Content is sent to the configured translation provider; optional AI is not invoked.
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
        :disabled="busy || !file"
      >
        {{ busy ? 'Working…' : 'Upload and translate' }}
      </button>
    </form>
    <div
      v-if="job"
      class="mt-7 border-t border-border pt-6"
      aria-live="polite"
    >
      <div class="mb-2 flex items-center justify-between text-sm">
        <span class="font-bold capitalize">{{ readableStage }}</span><span class="text-muted">{{ job.progress }}%</span>
      </div>
      <div
        class="h-2 overflow-hidden rounded-full bg-subtle"
        role="progressbar"
        :aria-valuenow="job.progress"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          class="h-full rounded-full bg-brand transition-all"
          :style="{ width: `${job.progress}%` }"
        />
      </div>
      <p
        v-if="job.state === 'failed'"
        class="mt-3 text-sm text-danger"
      >
        {{ job.error_message || 'The PDF could not be translated.' }}
      </p>
      <div
        v-if="job.state === 'completed'"
        class="mt-5"
      >
        <button
          class="button-primary"
          type="button"
          @click="download"
        >
          Download translated PDF
        </button><p class="mt-3 text-xs text-warning">
          Readable export: original visual layout is not preserved in this MVP.
        </p>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { ApiError } from '~/services/api'
import type { Job, Language } from '~/types/api'

export default defineComponent({
  name: 'PdfTranslator',
  props: { languages: { type: Array as PropType<Language[]>, required: true } },
  emits: ['updated'],
  data() {
    return { file: null as File | null, targetLanguage: 'hi', job: null as Job | null, busy: false, error: '', pollTimer: null as number | null }
  },
  computed: { readableStage(): string { return (this.job?.stage || 'queued').replace(/_/g, ' ') } },
  beforeUnmount() { this.stopPolling() },
  methods: {
    selectFile(event: Event): void {
      this.file = (event.target as HTMLInputElement).files?.[0] || null
      this.job = null
      this.error = ''
    },
    async checksum(file: File): Promise<string> {
      const digest = await crypto.subtle.digest('SHA-256', await file.arrayBuffer())
      return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('')
    },
    async start(): Promise<void> {
      if (!this.file) return
      this.busy = true
      this.error = ''
      this.job = null
      try {
        const intent = await this.$services.documents.createUpload(this.file, await this.checksum(this.file))
        await this.$services.documents.uploadToSignedUrl(intent, this.file)
        const completed = await this.$services.documents.completeUpload(intent.upload_id)
        this.job = await this.$services.documents.createTranslation(completed.document_id, this.targetLanguage)
        this.schedulePoll()
        this.$emit('updated')
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'The PDF workflow could not be started.'
        this.busy = false
      }
    },
    schedulePoll(): void {
      this.stopPolling()
      this.pollTimer = window.setTimeout(() => this.poll(), 1800)
    },
    stopPolling(): void {
      if (this.pollTimer !== null) window.clearTimeout(this.pollTimer)
      this.pollTimer = null
    },
    async poll(): Promise<void> {
      if (!this.job || ['completed', 'failed', 'cancelled'].includes(this.job.state)) {
        this.busy = false
        return
      }
      try {
        this.job = await this.$services.documents.getJob(this.job.id)
        if (['completed', 'failed', 'cancelled'].includes(this.job.state)) {
          this.busy = false
          this.$emit('updated')
          return
        }
        this.schedulePoll()
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'Progress could not be refreshed.'
        this.busy = false
      }
    },
    async download(): Promise<void> {
      if (!this.job?.output_file_id) return
      try {
        window.location.assign((await this.$services.documents.getDownloadUrl(this.job.output_file_id)).download_url)
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'The download could not be prepared.'
      }
    },
  },
})
</script>
