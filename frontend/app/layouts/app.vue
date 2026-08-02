<template>
  <div class="min-h-screen bg-canvas text-ink">
    <a
      href="#main-content"
      class="sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:not-sr-only focus:rounded-xl focus:bg-surface focus:px-4 focus:py-3"
    >Skip to workspace</a>
    <header class="sticky top-0 z-30 border-b border-border bg-surface/90 backdrop-blur-xl">
      <div class="page-shell flex min-h-20 items-center justify-between gap-4">
        <BrandMark />
        <div class="flex items-center gap-2">
          <LocaleSwitcher />
          <ThemeToggle />
          <button
            class="button-secondary !min-h-11 !px-4"
            type="button"
            @click="signOut"
          >
            {{ $t('actions.signOut') }}
          </button>
        </div>
      </div>
    </header>
    <main
      id="main-content"
      class="page-shell py-8 sm:py-12"
    >
      <slot />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useAuthStore } from '~/stores/auth'

export default defineComponent({
  name: 'WorkspaceLayout',
  methods: {
    async signOut(): Promise<void> {
      await useAuthStore().logout()
      await this.$router.replace(this.$localePath('/login'))
    },
  },
})
</script>
