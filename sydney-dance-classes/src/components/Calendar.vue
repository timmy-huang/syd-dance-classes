<template>
  <div class="d-flex align-center justify-content-center mt-5">
    <v-btn
      icon="mdi-chevron-left"
      variant="text"
      @click="$emit('previous-week')"
      aria-label="Previous week"
      density="comfortable"
      :color="disablePrevious ? 'grey' : undefined"
      :disabled="disablePrevious"
    ></v-btn>
    
    <div 
      :class="$vuetify.display.smAndDown ? 'scrollable-mobile' : 'desktop-view'"
      class="flex-grow-1"
    >
      <v-btn 
        variant="tonal" 
        v-for="date in datesForWeek" 
        :key="date.getTime()" 
        :active="date === selectedDate"
        @click="$emit('update', date)"
        style="height: auto; margin-right: 8px;"
      >
        <div style="flex-direction: column;" class="pa-2">
          <div>{{ date.getDate() }}/{{ date.getMonth() }}</div>
          <div>{{ days[date.getDay()] }}</div>
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
      :color="disableNext ? 'grey' : undefined"
      :disabled="disableNext"
    ></v-btn>
  </div>
</template>

<script lang="ts" setup>
  import { useDisplay } from 'vuetify'
  import { computed } from 'vue'
  
  const props = defineProps({
    selectedDate: Date,
    mondayDate: Date
  });

  let viewingCurrentWeek = true;

  const disablePrevious = true;
  const disableNext = true;

  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

  const datesForWeek = computed(() => {
    // if viewing current week, return the dates for the current week
    const arr : Date[] = [];
    if (viewingCurrentWeek) {
      for (let i = 0; i < 7; i++) {
        if (props.mondayDate) {
          arr.push(new Date(props.mondayDate.getTime() + i * 24 * 60 * 60 * 1000));
        }
      }
    } else {
      for (let i = 0; i < 7; i++) {
        if (props.mondayDate) {
          arr.push(new Date(props.mondayDate.getTime() + (i + 7) * 24 * 60 * 60 * 1000));
        }
      }
    }
    return arr;
  })

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