<template>
  <footer class="border-t border-border bg-surface">
    <div class="page-shell grid gap-10 py-12 md:grid-cols-[1.4fr_1fr_1fr]">
      <div>
        <BrandMark />
        <p class="mt-4 max-w-sm text-sm leading-6 text-muted">
          {{ $t('footer.description') }}
        </p>
      </div>
      <div>
        <p class="text-sm font-black">
          {{ $t('footer.product') }}
        </p>
        <div class="mt-4 grid gap-3 text-sm text-muted">
          <NuxtLink :to="$localePath('/features')">
            {{ $t('nav.features') }}
          </NuxtLink>
          <NuxtLink :to="$localePath('/pricing')">
            {{ $t('nav.pricing') }}
          </NuxtLink>
          <NuxtLink :to="$localePath('/docs')">
            {{ $t('nav.docs') }}
          </NuxtLink>
          <NuxtLink :to="$localePath('/contact')">
            {{ $t('nav.contact') }}
          </NuxtLink>
        </div>
      </div>
      <div>
        <p class="text-sm font-black">
          {{ $t('footer.legal') }}
        </p>
        <div class="mt-4 grid gap-3 text-sm text-muted">
          <NuxtLink :to="$localePath('/privacy')">
            {{ $t('nav.privacy') }}
          </NuxtLink>
          <NuxtLink :to="$localePath('/terms')">
            {{ $t('nav.terms') }}
          </NuxtLink>
          <a
            href="https://github.com/saurabhzaiswal"
            rel="me noopener"
            target="_blank"
          >{{ $t('footer.founderGitHub') }}</a>
        </div>
      </div>
    </div>
    <div class="border-t border-border">
      <div class="page-shell flex flex-col justify-between gap-2 py-5 text-xs text-muted sm:flex-row">
        <p>© {{ year }} Saurabh Choudhary. {{ $t('footer.rights') }}</p>
        <p>Aikya AI · One World. One Understanding.</p>
      </div>
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SiteFooter',
  computed: {
    year(): number {
      return new Date().getFullYear()
    },
  },
})
</script>
