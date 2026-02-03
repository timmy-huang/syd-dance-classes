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
      exclude: ['/', '/classes', '/classes/*', '/events', '/events/*', '/choreographer', '/choreographer/*', '/api/cg/**'], // Public pages
    }
  },


  routeRules: {
    '/api/classes': {
      headers: {
        'Cache-Control': 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=60'
      }
    },
    '/api/studios': {
      headers: {
        'Cache-Control': 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=60'
      }
    },
    '/api/cg/**': {
      cors: true,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
      }
    }
  },

  compatibilityDate: '2024-11-01'
})
