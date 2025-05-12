<template>
  <div :class="$vuetify.display.smAndDown ? 'scrollable-mobile' : 'desktop-view'" class="d-flex align-center justify-content-center mt-5">
    <v-btn
      v-if="!$vuetify.display.smAndDown"
      icon="mdi-chevron-left"
      variant="text"
      @click="handleLeftClick"
      aria-label="Previous week"
      density="comfortable"
      :color="disablePrevious ? 'grey' : undefined"
      :disabled="disablePrevious"
    ></v-btn>

    <div>
        <v-btn 
          variant="tonal" 
          v-for="date in datesForWeek" 
          :key="date.getTime()" 
          :active="date.getTime() === selectedDate!.getTime()"
          @click="$emit('update', date)"
        style="height: auto; margin-right: 8px; width: 122px;"
      >
        <div style="flex-direction: column;" class="pa-2">
          <div>{{ date.getDate() }}/{{ date.getMonth() }}</div>
          <div>{{ days[date.getDay()] }}</div>
        </div>
      </v-btn>
    </div>

    <v-btn
      v-if="!$vuetify.display.smAndDown"
      icon="mdi-chevron-right"
      variant="text"
      @click="handleRightClick"
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
  import { computed, ref } from 'vue'

  const emit = defineEmits(['update'])
  const display = useDisplay()

  const props = defineProps({
    selectedDate: Date,
    mondayDate: Date
  });

  const viewingCurrentWeek = ref(true);

  const disablePrevious = computed(() => {
    return viewingCurrentWeek.value;
  })

  const disableNext = computed(() => {
    return !viewingCurrentWeek.value;
  })

  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

  const datesForWeek = computed(() => {
    // if viewing current week, return the dates for the current week
    const arr : Date[] = [];
    // If mobile return both current and next week
    if (display.smAndDown.value) {
      for (let i = 0; i < 14; i++) {
        if (props.mondayDate) {
          arr.push(new Date(props.mondayDate.getTime() + i * 24 * 60 * 60 * 1000));
        } 
      }
    } else {
      if (viewingCurrentWeek.value) {
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
    }
    return arr;
  
  })

  const handleRightClick = () => {
    viewingCurrentWeek.value = false;
    emit('update', datesForWeek.value[0]);
  }

  const handleLeftClick = () => {
    viewingCurrentWeek.value = true;
    emit('update', datesForWeek.value[0]);
  }

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