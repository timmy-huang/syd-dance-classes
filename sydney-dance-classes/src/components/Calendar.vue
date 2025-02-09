<template>
  <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
    <div class="text-h2 mb-10">
      Class Schedule
    </div>
    <div style="display: flex; justify-content: space-between">
      <v-btn 
        variant="tonal" 
        v-for="day in days" 
        :key="day" 
        :active="days.indexOf(day) === selectedDay"
        :onClick="() => $emit('update', days.indexOf(day))"
        style="height: auto;"
      >
        <div style="flex-direction: column;" class="pa-2">
          <div>{{ mondayDate.getDate() + days.indexOf(day) }}/{{ mondayDate.getMonth() + 1 }}</div>
          <div>{{ day }}</div>
        </div>
        
      </v-btn>
    </div>
  </div>
</template>

<script lang="ts" setup>
  // Make a const for the days of the week
  const days: string[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const props = defineProps({
    selectedDay: Number,
    mondayDate: Date
  });
</script>