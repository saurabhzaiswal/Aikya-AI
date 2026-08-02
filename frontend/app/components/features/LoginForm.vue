<template>
  <UiCard
    class="auth-card"
    padding="none"
  >
    <div class="p-6 sm:p-8">
      <div class="mb-8">
        <span class="inline-flex items-center gap-2 rounded-full bg-brand-soft px-3 py-1.5 text-xs font-black text-brand-strong">
          <ShieldCheck
            :size="14"
            aria-hidden="true"
          />
          {{ $t('auth.login.badge') }}
        </span>
        <h1
          id="login-title"
          class="mt-5 text-3xl font-black tracking-[-0.035em] sm:text-4xl"
        >
          {{ $t('auth.login.title') }}
        </h1>
        <p class="mt-3 leading-7 text-muted">
          {{ $t('auth.login.description') }}
        </p>
      </div>

      <GoogleSignInButton :return-to="safeRedirectTarget" />

      <div class="auth-divider">
        <span />
        {{ $t('auth.google.orEmail') }}
        <span />
      </div>

      <form
        v-if="!mfaChallenge"
        novalidate
        class="space-y-5"
        aria-labelledby="login-title"
        @submit.prevent="submit"
      >
        <div>
          <label
            class="label"
            for="login-email"
          >{{ $t('auth.fields.email.label') }}</label>
          <div
            class="auth-field-shell"
            :class="{ 'auth-field-error': errors.email }"
          >
            <Mail
              class="auth-field-icon"
              :size="19"
              aria-hidden="true"
            />
            <input
              id="login-email"
              v-model.trim="email"
              class="auth-field-input"
              type="email"
              inputmode="email"
              autocomplete="email"
              :placeholder="$t('auth.fields.email.placeholder')"
              :aria-invalid="Boolean(errors.email)"
              :aria-describedby="errors.email ? 'login-email-error' : undefined"
              @blur="validateEmailField"
              @input="errors.email = ''"
            >
          </div>
          <p
            v-if="errors.email"
            id="login-email-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.email }}
          </p>
        </div>

        <div>
          <div class="mb-1.5 flex items-center justify-between gap-3">
            <label
              class="label !mb-0"
              for="login-password"
            >{{ $t('auth.fields.password.label') }}</label>
            <span class="text-xs font-semibold text-muted">{{ $t('auth.login.passwordHint') }}</span>
          </div>
          <div
            class="auth-field-shell"
            :class="{ 'auth-field-error': errors.password }"
          >
            <LockKeyhole
              class="auth-field-icon"
              :size="19"
              aria-hidden="true"
            />
            <input
              id="login-password"
              v-model="password"
              class="auth-field-input !pr-12"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              :placeholder="$t('auth.fields.password.loginPlaceholder')"
              :aria-invalid="Boolean(errors.password)"
              :aria-describedby="errors.password ? 'login-password-error' : undefined"
              @blur="validatePasswordField"
              @input="errors.password = ''"
            >
            <button
              class="auth-field-action"
              type="button"
              :aria-label="$t(showPassword ? 'auth.actions.hidePassword' : 'auth.actions.showPassword')"
              :aria-pressed="showPassword"
              @click="showPassword = !showPassword"
            >
              <EyeOff
                v-if="showPassword"
                :size="18"
                aria-hidden="true"
              />
              <Eye
                v-else
                :size="18"
                aria-hidden="true"
              />
            </button>
          </div>
          <p
            v-if="errors.password"
            id="login-password-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.password }}
          </p>
        </div>

        <div
          v-if="error"
          class="auth-error-panel"
          role="alert"
        >
          <CircleAlert
            class="mt-0.5 shrink-0"
            :size="18"
            aria-hidden="true"
          />
          <span>{{ error }}</span>
        </div>

        <button
          class="button-primary w-full"
          type="submit"
          :disabled="loading"
        >
          <span>{{ $t(loading ? 'auth.login.submitting' : 'auth.login.submit') }}</span>
          <LoaderCircle
            v-if="loading"
            class="animate-spin"
            :size="18"
            aria-hidden="true"
          />
          <ArrowRight
            v-else
            :size="18"
            aria-hidden="true"
          />
        </button>
      </form>

      <section
        v-else
        class="auth-mfa-panel"
        aria-labelledby="mfa-title"
      >
        <KeyRound
          class="text-brand"
          :size="28"
          aria-hidden="true"
        />
        <h2
          id="mfa-title"
          class="mt-4 text-xl font-black"
        >
          {{ $t('auth.mfa.title') }}
        </h2>
        <p class="mt-2 text-sm leading-6 text-muted">
          {{ $t('auth.mfa.description') }}
        </p>
        <p
          v-if="error"
          class="auth-error-panel mt-4 text-left"
          role="alert"
        >
          {{ error }}
        </p>
        <button
          class="button-primary mt-5 w-full"
          type="button"
          :disabled="loading"
          @click="verifyPasskey"
        >
          <Fingerprint
            :size="19"
            aria-hidden="true"
          />
          {{ $t('auth.mfa.usePasskey') }}
        </button>
        <button
          class="mt-3 w-full text-link"
          type="button"
          @click="useRecovery = !useRecovery"
        >
          {{ $t('auth.mfa.useRecovery') }}
        </button>
        <form
          v-if="useRecovery"
          class="mt-4 space-y-3"
          @submit.prevent="verifyRecovery"
        >
          <label
            class="label"
            for="recovery-code"
          >{{ $t('auth.mfa.recoveryLabel') }}</label>
          <input
            id="recovery-code"
            v-model.trim="recoveryCode"
            class="input"
            autocomplete="one-time-code"
            :placeholder="$t('auth.mfa.recoveryPlaceholder')"
          >
          <button
            class="button-secondary w-full"
            type="submit"
            :disabled="loading || !recoveryCode"
          >
            {{ $t('auth.mfa.verifyRecovery') }}
          </button>
        </form>
        <button
          class="mt-5 w-full text-sm font-bold text-muted hover:text-ink"
          type="button"
          @click="resetMfa"
        >
          {{ $t('auth.mfa.back') }}
        </button>
      </section>

      <div class="mt-7 flex items-center gap-3 text-xs font-bold uppercase tracking-[0.16em] text-muted">
        <span class="h-px flex-1 bg-border" />
        {{ $t('auth.login.newUser') }}
        <span class="h-px flex-1 bg-border" />
      </div>
      <NuxtLink
        class="button-secondary mt-5 w-full"
        :to="$localePath('/register')"
      >
        {{ $t('auth.login.createAccount') }}
      </NuxtLink>
    </div>

    <footer class="flex items-center justify-center gap-2 border-t border-border bg-subtle/45 px-6 py-4 text-center text-xs font-semibold text-muted">
      <LockKeyhole
        :size="14"
        aria-hidden="true"
      />
      {{ $t('auth.sessionProtected') }}
    </footer>
  </UiCard>
</template>

<script lang="ts">
import { startAuthentication } from '@simplewebauthn/browser'
import { ArrowRight, CircleAlert, Eye, EyeOff, Fingerprint, KeyRound, LoaderCircle, LockKeyhole, Mail, ShieldCheck } from '@lucide/vue'
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useAuthStore } from '~/stores/auth'
import { useToastStore } from '~/stores/toast'
import { isValidEmail } from '~/utils/auth-validation'
import type { WebAuthnRequiredResponse } from '~/types/api'

interface LoginErrors {
  email: string
  password: string
}

export default defineComponent({
  name: 'LoginForm',
  components: { ArrowRight, CircleAlert, Eye, EyeOff, Fingerprint, KeyRound, LoaderCircle, LockKeyhole, Mail, ShieldCheck },
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      loading: false,
      error: '',
      errors: { email: '', password: '' } as LoginErrors,
      mfaChallenge: null as WebAuthnRequiredResponse | null,
      recoveryCode: '',
      useRecovery: false,
      active: true,
    }
  },
  computed: {
    safeRedirectTarget(): string {
      const requested = typeof this.$route.query.redirect === 'string' ? this.$route.query.redirect : ''
      return requested.startsWith('/app/') ? requested : this.$localePath('/app/dashboard')
    },
  },
  async mounted() {
    const oauthError = typeof this.$route.query.oauth_error === 'string' ? this.$route.query.oauth_error : ''
    if (oauthError) {
      const supportedErrors = new Set([
        'google_not_configured',
        'google_cancelled',
        'google_oauth_failed',
        'google_identity_unverified',
        'google_account_link_failed',
        'invalid_oauth_state',
      ])
      this.error = supportedErrors.has(oauthError)
        ? String(this.$t(`auth.google.errors.${oauthError}`))
        : String(this.$t('auth.google.errors.google_oauth_failed'))
      useToastStore().push(this.error, 'error')
    }
    if (this.$route.query.oauth_mfa === 'required') {
      this.loading = true
      try {
        this.mfaChallenge = await this.$services.auth.pendingGoogleMfa()
        useToastStore().push(String(this.$t('auth.mfa.required')), 'info')
      }
      catch (caught) {
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('auth.mfa.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        this.loading = false
      }
    }
  },
  beforeUnmount() {
    this.active = false
  },
  methods: {
    async finishLogin(): Promise<void> {
      useToastStore().push(String(this.$t('auth.login.success')), 'success')
      await this.$router.replace(this.safeRedirectTarget)
    },
    resetMfa(): void {
      this.mfaChallenge = null
      this.recoveryCode = ''
      this.useRecovery = false
      this.error = ''
    },
    async verifyPasskey(): Promise<void> {
      if (!this.mfaChallenge) return
      this.loading = true
      this.error = ''
      try {
        const credential = await startAuthentication({ optionsJSON: this.mfaChallenge.options })
        if (!this.active) return
        await useAuthStore().completePasskeyLogin(this.mfaChallenge.challenge_id, credential)
        await this.finishLogin()
      }
      catch (caught) {
        if (!this.active) return
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('auth.mfa.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        if (this.active) this.loading = false
      }
    },
    async verifyRecovery(): Promise<void> {
      if (!this.mfaChallenge || !this.recoveryCode) return
      this.loading = true
      this.error = ''
      try {
        await useAuthStore().completeRecoveryLogin(this.mfaChallenge.challenge_id, this.recoveryCode)
        await this.finishLogin()
      }
      catch (caught) {
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('auth.mfa.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        this.loading = false
      }
    },
    validateEmailField(): boolean {
      this.errors.email = !this.email
        ? String(this.$t('auth.validation.emailRequired'))
        : isValidEmail(this.email) ? '' : String(this.$t('auth.validation.emailInvalid'))
      return !this.errors.email
    },
    validatePasswordField(): boolean {
      this.errors.password = this.password ? '' : String(this.$t('auth.validation.passwordRequired'))
      return !this.errors.password
    },
    validateForm(): boolean {
      return [this.validateEmailField(), this.validatePasswordField()].every(Boolean)
    },
    async submit(): Promise<void> {
      this.error = ''
      if (!this.validateForm()) {
        useToastStore().push(String(this.$t('auth.validation.correctFields')), 'error')
        return
      }

      this.loading = true
      try {
        this.mfaChallenge = await useAuthStore().login(this.email, this.password)
        if (this.mfaChallenge) {
          useToastStore().push(String(this.$t('auth.mfa.required')), 'info')
          return
        }
        await this.finishLogin()
      }
      catch (caught) {
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('auth.login.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        this.loading = false
      }
    },
  },
})
</script>
