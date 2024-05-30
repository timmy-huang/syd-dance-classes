<template>
  <v-card
    hover
    elevation="6"
    class="d-flex align-center"
  >

    <v-card-item class="lesson-card-item">
      <template v-slot:prepend>
        <StudioIcon :studio="lesson.studio" />
      </template> 
      <v-card-title>
        {{ lesson.name }}
      </v-card-title>
      <v-card-subtitle>
        {{ lesson.choreo }}
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <div class="text-subtitle-1">
        {{ formatDate(lesson.start) + " - " + formatDate(lesson.end) }}
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        variant="outlined"
        class="mr-4"
      >
        <a :href="bookLink" target="_blank" style="text-decoration: none; color: inherit;">
          Book Now
        </a>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
  
<script lang="ts" setup>
  import { Lesson } from '../utils/types'
  import { PropType } from 'vue'
  import { computed } from 'vue';

  const bookLink = computed(() => {
    if (props.lesson) {
      console.log(props.lesson.studio)
      if (props.lesson.studio === "movement_nation_hurstville") {
        return "https://www.movementnation.com.au/hurstville-bookings"
      }
      if (props.lesson.studio === "movement_nation_parramatta") {
        return "https://2020movementnation.wixsite.com/website-1"
      }
      if (props.lesson.studio === "imi") {
        return "https://imient.com.au/classes"
      }
    }
    console.log("Booking Link not found for ", props.lesson)
    return ""
  })

  const props = defineProps({
    lesson: Object as PropType<Lesson>,
  })

  const formatDate = (date: Date) => {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true }).replace(" ", "")
  }
</script>

<style>
  .v-card {
    margin: 1em;
  }

  .lesson-card-item {
    width: 500px;
  }
</style>