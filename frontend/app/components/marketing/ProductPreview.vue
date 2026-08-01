<template>
  <div
    class="relative mx-auto max-w-5xl"
    aria-label="Illustration of the Aikya AI translation workspace"
  >
    <div
      class="absolute -inset-8 rounded-[3rem] bg-brand/10 blur-3xl"
      aria-hidden="true"
    />
    <div class="glass-panel relative overflow-hidden rounded-[2rem] p-2 sm:p-3">
      <div class="flex items-center gap-2 border-b border-border px-4 py-3">
        <span
          v-for="color in dots"
          :key="color"
          class="size-2.5 rounded-full"
          :class="color"
        />
        <span class="ml-3 text-xs font-bold text-muted">Illustrative Phase 1 workspace</span>
      </div>
      <div class="grid gap-3 p-3 md:grid-cols-[0.72fr_1.28fr] md:p-5">
        <aside class="hidden rounded-2xl bg-canvas p-4 md:block">
          <div class="h-8 w-28 rounded-lg bg-brand-soft" />
          <div class="mt-6 space-y-3">
            <div
              v-for="width in widths"
              :key="width"
              class="h-3 rounded-full bg-subtle"
              :style="{ width }"
            />
          </div>
          <div class="mt-28 rounded-2xl border border-border bg-surface p-4">
            <p class="text-xs font-bold text-muted">
              Privacy default
            </p>
            <p class="mt-2 text-sm font-black">
              Temporary storage
            </p>
          </div>
        </aside>
        <div class="rounded-2xl bg-canvas p-4 sm:p-6">
          <div class="flex items-start justify-between gap-3">
            <div>
              <p class="eyebrow">
                Translate text
              </p>
              <p class="mt-2 text-xl font-black">
                English → हिन्दी
              </p>
            </div>
            <span class="rounded-full bg-accent-soft px-3 py-1 text-xs font-bold text-accent">Ready</span>
          </div>
          <div class="mt-6 grid gap-3 sm:grid-cols-2">
            <div class="min-h-36 rounded-2xl border border-border bg-surface p-4 text-sm leading-7 text-muted">
              Language should help people understand one another, not keep them apart.
            </div>
            <div
              class="min-h-36 rounded-2xl border border-brand/25 bg-brand-soft p-4 text-sm leading-7 text-ink"
              lang="hi"
            >
              भाषा लोगों को एक-दूसरे को समझने में मदद करे, उन्हें अलग न रखे।
            </div>
          </div>
          <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
            <span class="text-xs font-semibold text-muted">Text stays inside your workspace history.</span>
            <span class="button-primary !min-h-10 !px-4 text-sm">Translate text</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ProductPreview',
  data() {
    return {
      dots: ['bg-danger', 'bg-warning', 'bg-success'],
      widths: ['86%', '72%', '91%', '64%'],
    }
  },
})
</script>
