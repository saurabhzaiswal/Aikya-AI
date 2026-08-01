import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
  ignores: ['.nuxt/**', '.output/**', '.data/**', 'node_modules/**'],
}).append({
  files: ['app/components/**/*.vue'],
  rules: {
    'vue/component-api-style': ['error', ['options']],
    'vue/multi-word-component-names': 'off',
  },
})
