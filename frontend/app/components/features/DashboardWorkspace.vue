<template>
  <div>
    <header class="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
      <div>
        <p class="eyebrow">
          {{ auth.context?.workspace_name || 'Your workspace' }}
        </p><h1 class="mt-3 text-3xl font-black tracking-tight sm:text-5xl">
          Understand across languages.
        </h1><p class="mt-3 max-w-2xl leading-7 text-muted">
          Translate text or create a readable translation of a supported digital PDF.
        </p>
      </div>
      <p class="text-sm text-muted">
        Signed in as <span class="font-bold text-ink">{{ auth.user?.display_name }}</span>
      </p>
    </header>
    <p
      v-if="error"
      class="mb-6 rounded-xl bg-danger/10 p-4 text-sm text-danger"
      role="alert"
    >
      {{ error }}
    </p>
    <div class="grid items-start gap-6 lg:grid-cols-2">
      <TextTranslator
        :languages="languages"
        @translated="handleUpdated"
      /><PdfTranslator
        :languages="languages"
        @updated="handleUpdated"
      />
    </div>
    <section
      class="panel mt-6 p-5 sm:p-7"
      aria-labelledby="recent-title"
    >
      <div class="mb-5 flex items-center justify-between">
        <div>
          <p class="eyebrow !text-muted">
            Workspace
          </p><h2
            id="recent-title"
            class="mt-2 text-2xl font-black tracking-tight"
          >
            Recent activity
          </h2>
        </div><button
          class="ripple-control rounded-lg px-2 py-1 text-link text-sm"
          type="button"
          :disabled="loading"
          @click="loadDashboard"
        >
          Refresh
        </button>
      </div>
      <div
        v-if="loading"
        class="py-10 text-center text-muted"
        role="status"
      >
        Loading workspace…
      </div>
      <div
        v-else-if="!summary || (!summary.recent_documents.length && !summary.recent_translations.length)"
        class="rounded-2xl border border-dashed border-border p-10 text-center text-muted"
      >
        Your translations will appear here.
      </div>
      <div
        v-else
        class="grid gap-7 lg:grid-cols-2"
      >
        <div>
          <h3 class="mb-3 font-black">
            Documents
          </h3><ul class="space-y-2">
            <li
              v-for="document in summary.recent_documents"
              :key="document.id"
              class="flex items-center justify-between gap-3 rounded-2xl bg-canvas p-4"
            >
              <div class="min-w-0">
                <p class="truncate font-bold">
                  {{ document.title }}
                </p><p class="mt-1 text-xs text-muted">
                  {{ formatDate(document.created_at) }}
                </p>
              </div><span
                class="rounded-full px-2.5 py-1 text-xs font-bold capitalize"
                :class="statusClass(document.status)"
              >{{ document.status }}</span>
            </li>
          </ul>
        </div>
        <div>
          <h3 class="mb-3 font-black">
            Text translations
          </h3><ul class="space-y-2">
            <li
              v-for="translation in summary.recent_translations"
              :key="translation.id"
              class="rounded-2xl bg-canvas p-4"
            >
              <p class="truncate font-bold">
                {{ translation.translated_text }}
              </p><p class="mt-1 text-xs font-semibold uppercase tracking-wide text-muted">
                {{ translation.source_language }} → {{ translation.target_language }}
              </p>
            </li>
          </ul>
        </div>
      </div>
    </section>
    <PasskeySecurity />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useAuthStore } from '~/stores/auth'
import type { DashboardSummary, Language } from '~/types/api'

export default defineComponent({
  name: 'DashboardWorkspace',
  data() {
    return { auth: useAuthStore(), languages: [] as Language[], summary: null as DashboardSummary | null, loading: true, error: '' }
  },
  async mounted() {
    await Promise.all([this.loadLanguages(), this.loadDashboard()])
  },
  methods: {
    async loadLanguages(): Promise<void> {
      try {
        this.languages = await this.$services.translation.listLanguages()
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'Languages could not be loaded.'
      }
    },
    async loadDashboard(): Promise<void> {
      this.loading = true
      try {
        this.summary = await this.$services.dashboard.getSummary()
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'The dashboard could not be loaded.'
      }
      finally {
        this.loading = false
      }
    },
    handleUpdated(): void {
      void this.loadDashboard()
    },
    formatDate(value: string): string {
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
    },
    statusClass(status: string): string {
      if (status === 'completed') return 'bg-success/10 text-success'
      if (status === 'failed') return 'bg-danger/10 text-danger'
      return 'bg-warning/10 text-warning'
    },
  },
})
</script>
