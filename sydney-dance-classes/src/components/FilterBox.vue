<template>
  <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
    <v-text-field label="Label"></v-text-field>
  </div>
</template>

<script lang="ts" setup>
  // Make a const for the days of the week
  const days: string[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const props = defineProps({
    selectedDay: Number
  });
</script>