<template>
  <v-card class="no-classes-card text-center pa-6 my-5">
    <v-icon size="64" color="grey" class="mb-4">mdi-calendar-remove</v-icon>
    <h2 class="text-h5 mb-3">No Classes Found</h2>
    <p class="text-body-1">{{ message }}</p>
  </v-card>
</template>

<script lang="ts" setup>
defineProps({
  message: {
    type: String,
    default: 'Try adjusting your filters or search criteria to find more classes.'
  }
});
</script>

<style scoped>
.no-classes-card {
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
}
</style> 