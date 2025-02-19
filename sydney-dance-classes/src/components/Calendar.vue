<template>
  <div 
    :class="$vuetify.display.smAndDown ? 'scrollable-mobile' : 'desktop-view'"
    class="mt-5"
  >
    <v-btn 
      variant="tonal" 
      v-for="day in days" 
      :key="day" 
      :active="days.indexOf(day) === selectedDay"
      :onClick="() => $emit('update', days.indexOf(day))"
      style="height: auto; margin-right: 8px;"
    >
      <div style="flex-direction: column;" class="pa-2">
        <div>{{ mondayDate.getDate() + days.indexOf(day) }}/{{ mondayDate.getMonth() + 1 }}</div>
        <div>{{ day }}</div>
      </div>
    </v-btn>
  </div>
</template>

<script lang="ts" setup>
  import { useDisplay } from 'vuetify'
  const days: string[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const props = defineProps({
    selectedDay: Number,
    mondayDate: Date
  });
</script>

<style>
.scrollable-mobile {
  overflow-x: auto;
  white-space: nowrap;
  width: 100%;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.scrollable-mobile::-webkit-scrollbar {
  display: none;  /* Chrome, Safari, Opera */
}

.desktop-view {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
</style>