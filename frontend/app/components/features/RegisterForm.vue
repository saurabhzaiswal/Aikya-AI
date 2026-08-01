<template>
  <UiCard>
    <div class="mb-7 text-center">
      <p class="eyebrow">
        Phase 1 access
      </p>
      <h1
        id="register-title"
        class="mt-3 text-3xl font-black tracking-tight"
      >
        Create your workspace
      </h1>
      <p class="mt-2 text-muted">
        Start with private text and digital PDF translation.
      </p>
    </div>
    <form
      class="space-y-5"
      aria-labelledby="register-title"
      @submit.prevent="submit"
    >
      <div>
        <label
          class="label"
          for="display-name"
        >Name</label><input
          id="display-name"
          v-model.trim="displayName"
          class="field"
          autocomplete="name"
          minlength="2"
          required
        >
      </div>
      <div>
        <label
          class="label"
          for="register-email"
        >Email</label><input
          id="register-email"
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
          for="register-password"
        >Password</label>
        <input
          id="register-password"
          v-model="password"
          class="field"
          type="password"
          autocomplete="new-password"
          minlength="12"
          required
          aria-describedby="password-help"
        >
        <p
          id="password-help"
          class="mt-2 text-xs leading-5 text-muted"
        >
          Use 12+ characters and at least three of uppercase, lowercase, number, and symbol.
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
        class="button-primary w-full"
        type="submit"
        :disabled="loading"
      >
        {{ loading ? 'Creating workspace…' : 'Create account' }}
      </button>
    </form>
    <p class="mt-6 text-center text-sm text-muted">
      Already registered? <NuxtLink
        class="text-link"
        to="/login"
      >Sign in</NuxtLink>
    </p>
  </UiCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useAuthStore } from '~/stores/auth'

export default defineComponent({
  name: 'RegisterForm',
  data() {
    return { displayName: '', email: '', password: '', loading: false, error: '' }
  },
  methods: {
    async submit(): Promise<void> {
      this.loading = true
      this.error = ''
      try {
        await useAuthStore().register(this.displayName, this.email, this.password, this.$i18n.locale)
        await navigateTo('/app/dashboard')
      }
      catch (error) {
        this.error = error instanceof ApiError ? error.message : 'Your workspace could not be created.'
      }
      finally {
        this.loading = false
      }
    },
  },
})
</script>
