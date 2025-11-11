<template>
  <v-app>
    <!-- User menu in top right corner -->
    <div class='user-menu-container'>
      <UserMenu />
    </div>
    <div class="app-content">
      <NuxtPage />
      <Footer />
    </div>
  </v-app>
</template>

<script setup>
// Components are auto-imported in Nuxt
</script>

<style scoped>
.user-menu-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 1000;
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