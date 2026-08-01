<template>
  <button
    class="grid size-11 place-items-center rounded-xl border border-border bg-surface text-ink hover:border-brand/50 hover:bg-brand-soft"
    type="button"
    :aria-label="label"
    @click="toggle"
  >
    <Sun
      v-if="darkMode"
      :size="18"
      aria-hidden="true"
    />
    <Moon
      v-else
      :size="18"
      aria-hidden="true"
    />
  </button>
</template>

<script lang="ts">
import { Moon, Sun } from 'lucide-vue-next'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ThemeToggle',
  components: { Moon, Sun },
  data() {
    return { darkMode: false }
  },
  computed: {
    label(): string {
      return this.darkMode ? 'Switch to light theme' : 'Switch to dark theme'
    },
  },
  mounted() {
    const savedTheme = localStorage.getItem('aikya-theme')
    this.darkMode = savedTheme ? savedTheme === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches
    this.applyTheme()
  },
  methods: {
    applyTheme(): void {
      document.documentElement.classList.toggle('dark', this.darkMode)
    },
    toggle(): void {
      this.darkMode = !this.darkMode
      localStorage.setItem('aikya-theme', this.darkMode ? 'dark' : 'light')
      this.applyTheme()
    },
  },
})
</script>
