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
      exclude: ['/', '/classes', '/classes/*', '/events', '/events/*', '/choreographer', '/choreographer/*'], // Public pages
    }
  },


  routeRules: {
    '/api/cg/**': {
      cors: true,
      headers: {
        'Access-Control-Allow-Origin': 'https://choreoguessr.vercel.app/', // ✅ Only this domain
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Credentials': 'true'
      }
    }
  },

  compatibilityDate: '2024-11-01'
})
