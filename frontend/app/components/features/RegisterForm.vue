<template>
  <UiCard
    class="auth-card"
    padding="none"
  >
    <div class="p-6 sm:p-8">
      <div class="mb-8">
        <span class="inline-flex items-center gap-2 rounded-full bg-brand-soft px-3 py-1.5 text-xs font-black text-brand-strong">
          <Sparkles
            :size="14"
            aria-hidden="true"
          />
          {{ $t('auth.register.badge') }}
        </span>
        <h1
          id="register-title"
          class="mt-5 text-3xl font-black tracking-[-0.035em] sm:text-4xl"
        >
          {{ $t('auth.register.title') }}
        </h1>
        <p class="mt-3 leading-7 text-muted">
          {{ $t('auth.register.description') }}
        </p>
      </div>

      <GoogleSignInButton />

      <div class="auth-divider">
        <span />
        {{ $t('auth.google.orEmail') }}
        <span />
      </div>

      <form
        novalidate
        class="space-y-5"
        aria-labelledby="register-title"
        @submit.prevent="submit"
      >
        <div>
          <label
            class="label"
            for="display-name"
          >{{ $t('auth.fields.name.label') }}</label>
          <div
            class="auth-field-shell"
            :class="{ 'auth-field-error': errors.displayName }"
          >
            <UserRound
              class="auth-field-icon"
              :size="19"
              aria-hidden="true"
            />
            <input
              id="display-name"
              v-model.trim="displayName"
              class="auth-field-input"
              autocomplete="name"
              maxlength="120"
              :placeholder="$t('auth.fields.name.placeholder')"
              :aria-invalid="Boolean(errors.displayName)"
              :aria-describedby="errors.displayName ? 'display-name-error' : undefined"
              @blur="validateNameField"
              @input="errors.displayName = ''"
            >
          </div>
          <p
            v-if="errors.displayName"
            id="display-name-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.displayName }}
          </p>
        </div>

        <div>
          <label
            class="label"
            for="register-email"
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
              id="register-email"
              v-model.trim="email"
              class="auth-field-input"
              type="email"
              inputmode="email"
              autocomplete="email"
              :placeholder="$t('auth.fields.email.placeholder')"
              :aria-invalid="Boolean(errors.email)"
              :aria-describedby="errors.email ? 'register-email-error' : undefined"
              @blur="validateEmailField"
              @input="errors.email = ''"
            >
          </div>
          <p
            v-if="errors.email"
            id="register-email-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.email }}
          </p>
        </div>

        <div>
          <label
            class="label"
            for="register-password"
          >{{ $t('auth.fields.password.createLabel') }}</label>
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
              id="register-password"
              v-model="password"
              class="auth-field-input !pr-12"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              maxlength="128"
              :placeholder="$t('auth.fields.password.createPlaceholder')"
              :aria-invalid="Boolean(errors.password)"
              :aria-describedby="errors.password ? 'register-password-error password-checks' : 'password-checks'"
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
            id="register-password-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.password }}
          </p>
          <ul
            id="password-checks"
            class="mt-3 grid gap-2 text-xs sm:grid-cols-2"
            aria-live="polite"
          >
            <li :class="passwordRuleClass(passwordChecks.hasLength)">
              <CircleCheck
                :size="14"
                aria-hidden="true"
              /> {{ $t('auth.passwordRules.length') }}
            </li>
            <li :class="passwordRuleClass(passwordChecks.hasUppercase)">
              <CircleCheck
                :size="14"
                aria-hidden="true"
              /> {{ $t('auth.passwordRules.uppercase') }}
            </li>
            <li :class="passwordRuleClass(passwordChecks.hasLowercase)">
              <CircleCheck
                :size="14"
                aria-hidden="true"
              /> {{ $t('auth.passwordRules.lowercase') }}
            </li>
            <li :class="passwordRuleClass(passwordChecks.hasNumber)">
              <CircleCheck
                :size="14"
                aria-hidden="true"
              /> {{ $t('auth.passwordRules.number') }}
            </li>
            <li :class="passwordRuleClass(passwordChecks.hasSymbol)">
              <CircleCheck
                :size="14"
                aria-hidden="true"
              /> {{ $t('auth.passwordRules.symbol') }}
            </li>
          </ul>
        </div>

        <div>
          <label
            class="label"
            for="confirm-password"
          >{{ $t('auth.fields.confirmPassword.label') }}</label>
          <div
            class="auth-field-shell"
            :class="{ 'auth-field-error': errors.confirmPassword }"
          >
            <KeyRound
              class="auth-field-icon"
              :size="19"
              aria-hidden="true"
            />
            <input
              id="confirm-password"
              v-model="confirmPassword"
              class="auth-field-input"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              :placeholder="$t('auth.fields.confirmPassword.placeholder')"
              :aria-invalid="Boolean(errors.confirmPassword)"
              :aria-describedby="errors.confirmPassword ? 'confirm-password-error' : undefined"
              @blur="validateConfirmPasswordField"
              @input="errors.confirmPassword = ''"
            >
          </div>
          <p
            v-if="errors.confirmPassword"
            id="confirm-password-error"
            class="auth-field-message"
            role="alert"
          >
            {{ errors.confirmPassword }}
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
          <span>{{ $t(loading ? 'auth.register.submitting' : 'auth.register.submit') }}</span>
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

        <p class="text-center text-xs leading-5 text-muted">
          {{ $t('auth.register.agreementPrefix') }}
          <NuxtLink
            class="text-link"
            :to="$localePath('/terms')"
          >{{ $t('nav.terms') }}</NuxtLink>
          {{ $t('auth.register.agreementJoin') }}
          <NuxtLink
            class="text-link"
            :to="$localePath('/privacy')"
          >{{ $t('nav.privacy') }}</NuxtLink>.
        </p>
      </form>

      <div class="mt-7 flex items-center gap-3 text-xs font-bold uppercase tracking-[0.16em] text-muted">
        <span class="h-px flex-1 bg-border" />
        {{ $t('auth.register.existingUser') }}
        <span class="h-px flex-1 bg-border" />
      </div>
      <NuxtLink
        class="button-secondary mt-5 w-full"
        :to="$localePath('/login')"
      >
        {{ $t('auth.register.signIn') }}
      </NuxtLink>
    </div>
  </UiCard>
</template>

<script lang="ts">
import { ArrowRight, CircleAlert, CircleCheck, Eye, EyeOff, KeyRound, LoaderCircle, LockKeyhole, Mail, Sparkles, UserRound } from '@lucide/vue'
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useAuthStore } from '~/stores/auth'
import { useToastStore } from '~/stores/toast'
import { getPasswordChecks, isValidEmail, type PasswordChecks } from '~/utils/auth-validation'

interface RegisterErrors {
  displayName: string
  email: string
  password: string
  confirmPassword: string
}

export default defineComponent({
  name: 'RegisterForm',
  components: { ArrowRight, CircleAlert, CircleCheck, Eye, EyeOff, KeyRound, LoaderCircle, LockKeyhole, Mail, Sparkles, UserRound },
  data() {
    return {
      displayName: '',
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      loading: false,
      error: '',
      errors: { displayName: '', email: '', password: '', confirmPassword: '' } as RegisterErrors,
    }
  },
  computed: {
    passwordChecks(): PasswordChecks {
      return getPasswordChecks(this.password)
    },
  },
  methods: {
    passwordRuleClass(passed: boolean): string {
      return `flex items-center gap-2 font-semibold ${passed ? 'text-success' : 'text-muted'}`
    },
    validateNameField(): boolean {
      this.errors.displayName = this.displayName.length >= 2 && this.displayName.length <= 120
        ? ''
        : String(this.$t('auth.validation.nameLength'))
      return !this.errors.displayName
    },
    validateEmailField(): boolean {
      this.errors.email = !this.email
        ? String(this.$t('auth.validation.emailRequired'))
        : isValidEmail(this.email) ? '' : String(this.$t('auth.validation.emailInvalid'))
      return !this.errors.email
    },
    validatePasswordField(): boolean {
      this.errors.password = this.passwordChecks.isValid ? '' : String(this.$t('auth.validation.passwordStrength'))
      return !this.errors.password
    },
    validateConfirmPasswordField(): boolean {
      this.errors.confirmPassword = this.confirmPassword && this.confirmPassword === this.password
        ? ''
        : String(this.$t('auth.validation.passwordMismatch'))
      return !this.errors.confirmPassword
    },
    validateForm(): boolean {
      return [
        this.validateNameField(),
        this.validateEmailField(),
        this.validatePasswordField(),
        this.validateConfirmPasswordField(),
      ].every(Boolean)
    },
    async submit(): Promise<void> {
      this.error = ''
      if (!this.validateForm()) {
        useToastStore().push(String(this.$t('auth.validation.correctFields')), 'error')
        return
      }

      this.loading = true
      try {
        await useAuthStore().register(this.displayName, this.email, this.password, this.$i18n.locale)
        useToastStore().push(String(this.$t('auth.register.success')), 'success')
        await this.$router.replace(this.$localePath('/app/dashboard'))
      }
      catch (caught) {
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('auth.register.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        this.loading = false
      }
    },
  },
})
</script>
