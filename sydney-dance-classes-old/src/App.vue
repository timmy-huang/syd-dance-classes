<template>
  <Analytics />
  <v-app>
    <v-main>
      <router-view />
    </v-main>
    <Footer />
  </v-app>
</template>

<script lang="ts" setup>
  import { Analytics } from '@vercel/analytics/vue';

</script>

<style>
  .v-application {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
</style>
