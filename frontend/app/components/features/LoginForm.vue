<template>
  <UiCard>
    <div class="mb-7 text-center">
      <p class="eyebrow">
        Private workspace
      </p>
      <h1
        id="login-title"
        class="mt-3 text-3xl font-black tracking-tight"
      >
        Welcome back
      </h1>
      <p class="mt-2 text-muted">
        Continue to your language workspace.
      </p>
    </div>
    <form
      class="space-y-5"
      aria-labelledby="login-title"
      @submit.prevent="submit"
    >
      <div>
        <label
          class="label"
          for="email"
        >Email</label><input
          id="email"
          v-model.trim="email"
          class="field"
          type="email"
          autocomplete="email"
          required
        >
      </div>
      <div>
        <label
          class="label"
          for="password"
        >Password</label><input
          id="password"
          v-model="password"
          class="field"
          type="password"
          autocomplete="current-password"
          required
        >
      </div>
      <p
        v-if="error"
        class="rounded-xl bg-danger/10 p-3 text-sm text-danger"
        role="alert"
      >
        {{ error }}
      </p>
      <button
        class="button-primary w-full"
        type="submit"
        :disabled="loading"
      >
        {{ loading ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
    <p class="mt-6 text-center text-sm text-muted">
      New to Aikya? <NuxtLink
        class="text-link"
        to="/register"
      >Create an account</NuxtLink>
    </p>
  </UiCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useAuthStore } from '~/stores/auth'

export default defineComponent({
  name: 'LoginForm',
  data() {
    return { email: '', password: '', loading: false, error: '' }
  },
  methods: {
    async submit(): Promise<void> {
      this.loading = true
      this.error = ''
      try {
        await useAuthStore().login(this.email, this.password)
        const requestedPath = typeof this.$route.query.redirect === 'string' ? this.$route.query.redirect : '/app/dashboard'
        // Only internal application paths are accepted as post-login redirects.
        await navigateTo(requestedPath.startsWith('/app/') ? requestedPath : '/app/dashboard')
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'Sign in could not be completed.'
      }
      finally {
        this.loading = false
      }
    },
  },
})
</script>
