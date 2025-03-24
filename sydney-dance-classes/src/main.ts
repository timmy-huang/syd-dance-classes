/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import router from './router'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')

// Handle redirect from sessionStorage after app is mounted
router.isReady().then(() => {
  const redirect = sessionStorage.redirect
  if (redirect) {
    delete sessionStorage.redirect
    router.push(redirect)
  }
})