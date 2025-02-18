<template>
  <div class="scrollable-container mt-5">
    <div class="days-wrapper">
      <v-btn 
        variant="tonal" 
        v-for="day in days" 
        :key="day" 
        :active="days.indexOf(day) === selectedDay"
        :onClick="() => $emit('update', days.indexOf(day))"
        style="height: auto;"
        class="day-btn"
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
  const days: string[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const props = defineProps({
    selectedDay: Number,
    mondayDate: Date
  });
</script>

<style>
.scrollable-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* For smooth scrolling on iOS */
}

.days-wrapper {
  display: flex;
  gap: 8px; /* Adds consistent spacing between buttons */
  padding: 0 4px; /* Optional: adds some padding at the edges */
  min-width: min-content; /* Ensures content doesn't wrap */
}

.day-btn {
  flex: 0 0 auto; /* Prevents button from shrinking */
}

/* Hide scrollbar for Chrome, Safari and Opera */
.scrollable-container::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.scrollable-container {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>