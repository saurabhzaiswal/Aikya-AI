<template>
  <div class="relative min-h-screen overflow-hidden bg-canvas text-ink lg:grid lg:grid-cols-[1.05fr_0.95fr]">
    <section class="relative hidden overflow-hidden border-r border-border bg-brand-strong px-10 py-12 text-on-brand lg:flex lg:flex-col xl:px-16">
      <div
        class="site-grid pointer-events-none absolute inset-0 opacity-20"
        aria-hidden="true"
      />
      <div
        class="pointer-events-none absolute -left-24 top-1/4 size-96 rounded-full bg-accent/20 blur-3xl"
        aria-hidden="true"
      />
      <div
        class="pointer-events-none absolute -bottom-24 right-0 size-96 rounded-full bg-on-brand/10 blur-3xl"
        aria-hidden="true"
      />

      <NuxtLink
        class="relative z-10 inline-flex w-fit items-center gap-3"
        :to="$localePath('/')"
      >
        <span class="grid size-11 place-items-center rounded-2xl bg-on-brand text-xl font-black text-brand-strong shadow-xl">A</span>
        <span>
          <span class="block text-lg font-black leading-none">Aikya AI</span>
          <span class="mt-1 block text-xs font-semibold text-on-brand/70">{{ $t('auth.brandTagline') }}</span>
        </span>
      </NuxtLink>

      <div class="relative z-10 my-auto max-w-xl py-16">
        <p class="text-xs font-black uppercase tracking-[0.24em] text-on-brand/65">
          {{ $t('auth.privateWorkspace') }}
        </p>
        <h1 class="mt-5 text-balance text-5xl font-black leading-[1.04] tracking-[-0.045em] xl:text-6xl">
          {{ $t('auth.heroTitle') }}
        </h1>
        <p class="mt-6 max-w-lg text-lg leading-8 text-on-brand/75">
          {{ $t('auth.heroDescription') }}
        </p>
        <ul
          class="mt-10 grid gap-5"
          role="list"
        >
          <li
            v-for="benefit in benefits"
            :key="benefit.key"
            class="flex items-start gap-3"
          >
            <span class="mt-0.5 grid size-7 shrink-0 place-items-center rounded-full bg-on-brand/12">
              <component
                :is="benefit.icon"
                :size="15"
                aria-hidden="true"
              />
            </span>
            <span>
              <strong class="block text-sm font-black">{{ $t(`auth.benefits.${benefit.key}.title`) }}</strong>
              <span class="mt-1 block text-sm leading-6 text-on-brand/65">{{ $t(`auth.benefits.${benefit.key}.description`) }}</span>
            </span>
          </li>
        </ul>
      </div>

      <p class="relative z-10 text-xs font-semibold text-on-brand/55">
        {{ $t('auth.securityNote') }}
      </p>
    </section>

    <main class="relative flex min-h-screen items-center justify-center px-4 py-8 sm:px-8 lg:px-10 xl:px-16">
      <div
        class="site-grid pointer-events-none absolute inset-0 opacity-60"
        aria-hidden="true"
      />
      <div
        class="pointer-events-none absolute right-[10%] top-[8%] size-72 rounded-full bg-brand/10 blur-3xl"
        aria-hidden="true"
      />

      <div class="absolute left-4 top-4 z-20 lg:hidden">
        <BrandMark :show-tagline="false" />
      </div>
      <div class="absolute right-4 top-4 z-20">
        <LocaleSwitcher />
      </div>

      <div class="relative z-10 w-full max-w-[31rem] pt-20 lg:pt-0">
        <slot />
        <p class="mt-6 text-center text-sm font-semibold text-muted">
          <NuxtLink
            class="inline-flex items-center gap-2 rounded-lg px-2 py-1 hover:bg-subtle hover:text-ink"
            :to="$localePath('/')"
          >
            <ArrowLeft
              :size="16"
              aria-hidden="true"
            />
            {{ $t('auth.backHome') }}
          </NuxtLink>
        </p>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { ArrowLeft, FileText, Languages, ShieldCheck } from '@lucide/vue'
import { defineComponent, markRaw } from 'vue'

export default defineComponent({
  name: 'AuthLayout',
  components: { ArrowLeft, FileText, Languages, ShieldCheck },
  data() {
    return {
      benefits: [
        { key: 'privacy', icon: markRaw(ShieldCheck) },
        { key: 'languages', icon: markRaw(Languages) },
        { key: 'documents', icon: markRaw(FileText) },
      ],
    }
  },
})
</script>
