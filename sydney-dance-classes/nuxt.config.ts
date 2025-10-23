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
    async (options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        config.plugins ||= []
        config.plugins.push(vuetify({ autoImport: true }))
      })
    }
  ],

  compatibilityDate: '2024-11-01'
})
