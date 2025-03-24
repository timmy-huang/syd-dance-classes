/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHashHistory } from 'vue-router/auto'

const router = createRouter({
  // Use hash history instead of web history for GitHub Pages compatibility
  history: createWebHashHistory(import.meta.env.BASE_URL),
})

export default router
