<template>
  <section
    class="panel mt-6 p-5 sm:p-7"
    aria-labelledby="passkey-title"
  >
    <div class="flex flex-col justify-between gap-5 sm:flex-row sm:items-start">
      <div class="max-w-2xl">
        <div class="flex items-center gap-3">
          <span class="grid size-11 place-items-center rounded-xl bg-brand-soft text-brand">
            <Fingerprint
              :size="23"
              aria-hidden="true"
            />
          </span>
          <div>
            <p class="eyebrow">
              {{ $t('security.passkeys.eyebrow') }}
            </p>
            <h2
              id="passkey-title"
              class="mt-1 text-2xl font-black tracking-tight"
            >
              {{ $t('security.passkeys.title') }}
            </h2>
          </div>
        </div>
        <p class="mt-4 text-sm leading-6 text-muted">
          {{ $t('security.passkeys.description') }}
        </p>
      </div>
      <button
        class="button-secondary shrink-0"
        type="button"
        :disabled="loading || !supported"
        @click="enroll"
      >
        <LoaderCircle
          v-if="loading"
          class="animate-spin"
          :size="18"
          aria-hidden="true"
        />
        <Plus
          v-else
          :size="18"
          aria-hidden="true"
        />
        {{ $t(status?.enabled ? 'security.passkeys.addAnother' : 'security.passkeys.enable') }}
      </button>
    </div>

    <p
      v-if="!supported"
      class="auth-error-panel mt-5"
      role="status"
    >
      {{ $t('security.passkeys.unsupported') }}
    </p>
    <p
      v-if="error"
      class="auth-error-panel mt-5"
      role="alert"
    >
      {{ error }}
    </p>

    <ul
      v-if="status?.credentials.length"
      class="mt-5 grid gap-3 sm:grid-cols-2"
    >
      <li
        v-for="credential in status.credentials"
        :key="credential.id"
        class="rounded-2xl border border-border bg-canvas p-4"
      >
        <p class="flex items-center gap-2 font-black">
          <CircleCheck
            class="text-success"
            :size="17"
            aria-hidden="true"
          />
          {{ credential.name }}
        </p>
        <p class="mt-2 text-xs text-muted">
          {{ $t('security.passkeys.added', { date: formatDate(credential.created_at) }) }}
        </p>
      </li>
    </ul>

    <div
      v-if="recoveryCodes.length"
      class="mt-6 rounded-2xl border border-warning/30 bg-warning/10 p-5"
      role="status"
    >
      <h3 class="font-black">
        {{ $t('security.passkeys.recoveryTitle') }}
      </h3>
      <p class="mt-2 text-sm leading-6 text-muted">
        {{ $t('security.passkeys.recoveryDescription') }}
      </p>
      <ul class="mt-4 grid gap-2 font-mono text-sm font-bold sm:grid-cols-2">
        <li
          v-for="code in recoveryCodes"
          :key="code"
          class="rounded-lg border border-border bg-surface px-3 py-2"
        >
          {{ code }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script lang="ts">
import { browserSupportsWebAuthn, startRegistration } from '@simplewebauthn/browser'
import { CircleCheck, Fingerprint, LoaderCircle, Plus } from '@lucide/vue'
import { defineComponent } from 'vue'
import { ApiError } from '~/services/api'
import { useToastStore } from '~/stores/toast'
import type { WebAuthnStatusResponse } from '~/types/api'

export default defineComponent({
  name: 'PasskeySecurity',
  components: { CircleCheck, Fingerprint, LoaderCircle, Plus },
  data() {
    return {
      status: null as WebAuthnStatusResponse | null,
      recoveryCodes: [] as string[],
      supported: false,
      loading: false,
      error: '',
      active: true,
    }
  },
  async mounted() {
    this.supported = browserSupportsWebAuthn()
    await this.loadStatus()
  },
  beforeUnmount() {
    this.active = false
  },
  methods: {
    async loadStatus(): Promise<void> {
      try {
        this.status = await this.$services.auth.webauthnStatus()
      }
      catch (caught) {
        if (this.active) this.error = caught instanceof ApiError ? caught.message : String(this.$t('security.passkeys.statusFailure'))
      }
    },
    async enroll(): Promise<void> {
      if (!this.supported) return
      this.loading = true
      this.error = ''
      try {
        const options = await this.$services.auth.webauthnRegistrationOptions()
        const credential = await startRegistration({ optionsJSON: options.options })
        if (!this.active) return
        const result = await this.$services.auth.verifyWebAuthnRegistration(options.challenge_id, credential)
        this.recoveryCodes = result.recovery_codes
        await this.loadStatus()
        useToastStore().push(String(this.$t('security.passkeys.success')), 'success')
      }
      catch (caught) {
        if (!this.active) return
        this.error = caught instanceof ApiError ? caught.message : String(this.$t('security.passkeys.failure'))
        useToastStore().push(this.error, 'error')
      }
      finally {
        if (this.active) this.loading = false
      }
    },
    formatDate(value: string): string {
      return new Intl.DateTimeFormat(this.$i18n.locale, { dateStyle: 'medium' }).format(new Date(value))
    },
  },
})
</script>
