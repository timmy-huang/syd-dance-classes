<template>
  <v-app>
    <!-- Header with tabs and user menu -->
    <header class="app-header">
      <ClientOnly>
        <v-tabs
          :model-value="activeTab"
          color="primary"
          class="header-tabs"
          centered
          :touch="false"
          height="60"
        >
          <template v-if="isGenericApplicationPage">
            <v-tab
              value="application-home"
              :size="tabSize"
              @click="navigateTo('/application-home')"
            >
              App Home
            </v-tab>
            <v-tab
              value="privacy-policy"
              :size="tabSize"
              @click="navigateTo('/privacy-policy')"
            >
              Privacy
            </v-tab>
          </template>
          <template v-else>
            <v-tab
              value="classes"
              :size="tabSize"
              @click="navigateTo('/classes')"
            >
              Classes
            </v-tab>
            <v-tab
              value="events"
              :size="tabSize"
              @click="navigateTo('/events')"
            >
              Events
            </v-tab>
          </template>
        </v-tabs>
      </ClientOnly>
      <div class='user-menu-container'>
        <UserMenu />
      </div>
    </header>
    <div class="app-content">
      <NuxtPage />
      <Footer />
    </div>
  </v-app>
</template>

<script setup>
const route = useRoute()
const genericApplicationRoutes = ['/application-home', '/privacy-policy']

const isGenericApplicationPage = computed(() => {
  return genericApplicationRoutes.includes(route.path)
})

// Determine active tab based on current route
const activeTab = computed(() => {
  const path = route.path
  if (path === '/application-home') {
    return 'application-home'
  }
  if (path === '/privacy-policy') {
    return 'privacy-policy'
  }
  if (path.startsWith('/events')) {
    return 'events'
  }
  if (path.startsWith('/classes')) {
    return 'classes'
  }
  // Default to classes for index, classes, or any other route
  return ''
})

// Responsive tab size
const tabSize = computed(() => {
  return 'large'
})
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
}

.header-tabs {
  flex: 1;
  max-width: 975px;
}

.user-menu-container {
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  z-index: 1001;
}

.app-content {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-content > :first-child {
  flex: 1;
}
</style>
