<template>
  <div class="d-flex align-center justify-content-center mt-5">
    <v-btn
      icon="mdi-chevron-left"
      variant="text"
      @click="$emit('previous-week')"
      aria-label="Previous week"
      density="comfortable"
    ></v-btn>
    
    <div 
      :class="$vuetify.display.smAndDown ? 'scrollable-mobile' : 'desktop-view'"
      class="flex-grow-1"
    >
      <v-btn 
        variant="tonal" 
        v-for="day in days" 
        :key="day" 
        :active="days.indexOf(day) === selectedDay"
        @click="$emit('update', days.indexOf(day))"
        style="height: auto; margin-right: 8px;"
      >
        <div style="flex-direction: column;" class="pa-2">
          <div>{{ mondayDate.getDate() + days.indexOf(day) }}/{{ mondayDate.getMonth() + 1 }}</div>
          <div>{{ day }}</div>
        </div>
      </v-btn>
    </div>
    
    <v-btn
      icon="mdi-chevron-right"
      variant="text"
      @click="$emit('next-week')"
      aria-label="Next week"
      density="comfortable"
      style="margin-left: -8px;"
    ></v-btn>
  </div>
</template>

<script lang="ts" setup>
  import { useDisplay } from 'vuetify'
  const days: string[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const props = defineProps({
    selectedDay: Number,
    mondayDate: Date
  });

  defineEmits(['update', 'previous-week', 'next-week']);
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