<template>
  <header class="sticky top-0 z-40 border-b border-border/70 bg-canvas/85 backdrop-blur-xl">
    <div class="page-shell flex min-h-20 items-center justify-between gap-5">
      <BrandMark />
      <nav
        class="hidden items-center gap-1 md:flex"
        :aria-label="$t('accessibility.mainNavigation')"
      >
        <NuxtLink
          v-for="item in navigation"
          :key="item.to"
          class="rounded-xl px-3 py-2 text-sm font-bold text-muted hover:bg-subtle hover:text-ink"
          active-class="!text-brand"
          :to="$localePath(item.to)"
        >
          {{ $t(item.labelKey) }}
        </NuxtLink>
      </nav>
      <div class="flex items-center gap-2">
        <ThemeToggle />
        <LocaleSwitcher class="hidden lg:flex" />
        <NuxtLink
          class="hidden min-h-11 items-center rounded-xl px-3 font-bold text-muted hover:text-ink sm:inline-flex"
          :to="$localePath('/login')"
        >
          {{ $t('actions.signIn') }}
        </NuxtLink>
        <NuxtLink
          class="button-primary !min-h-11 !px-4"
          :to="$localePath('/register')"
        >
          {{ $t('actions.startTranslating') }}
        </NuxtLink>
        <button
          class="ripple-control grid size-11 place-items-center rounded-xl border border-border md:hidden"
          type="button"
          :aria-expanded="menuOpen"
          aria-controls="mobile-navigation"
          :aria-label="$t('accessibility.toggleNavigation')"
          @click="menuOpen = !menuOpen"
        >
          <X
            v-if="menuOpen"
            :size="20"
            aria-hidden="true"
          />
          <MenuIcon
            v-else
            :size="20"
            aria-hidden="true"
          />
        </button>
      </div>
    </div>
    <nav
      v-if="menuOpen"
      id="mobile-navigation"
      class="page-shell grid gap-1 border-t border-border py-3 md:hidden"
      :aria-label="$t('accessibility.mobileNavigation')"
    >
      <NuxtLink
        v-for="item in navigation"
        :key="item.to"
        class="rounded-xl px-3 py-3 font-bold text-muted hover:bg-subtle hover:text-ink"
        :to="$localePath(item.to)"
        @click="menuOpen = false"
      >
        {{ $t(item.labelKey) }}
      </NuxtLink>
      <LocaleSwitcher class="mt-2 w-fit lg:hidden" />
      <NuxtLink
        class="rounded-xl px-3 py-3 font-bold text-muted sm:hidden"
        :to="$localePath('/login')"
        @click="menuOpen = false"
      >
        {{ $t('actions.signIn') }}
      </NuxtLink>
    </nav>
  </header>
</template>

<script lang="ts">
import { Menu as MenuIcon, X } from '@lucide/vue'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SiteHeader',
  components: { MenuIcon, X },
  data() {
    return {
      menuOpen: false,
      navigation: [
        { labelKey: 'nav.features', to: '/features' },
        { labelKey: 'nav.pricing', to: '/pricing' },
        { labelKey: 'nav.blog', to: '/blog' },
        { labelKey: 'nav.docs', to: '/docs' },
        { labelKey: 'nav.about', to: '/about' },
      ],
    }
  },
})
</script>
