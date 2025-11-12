import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  devtools: { enabled: true },

  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
  ],


  build: {
    transpile: ['vuetify'],
  },
  plugins: ['~/plugins/vuetify.ts'],
  modules: [
    '@nuxtjs/supabase',
    async (options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        config.plugins ||= []
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
  ],

  supabase: {
    // Redirects
    redirectOptions: {
      login: '/login',
      callback: '/confirm',
      exclude: ['/', '/classes', '/classes/*', '/choreographer', '/choreographer/*'], // Public pages
    }
  },

  compatibilityDate: '2024-11-01'
})
