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
        text="Book Now"
        class="mr-4"
      />
    </v-card-actions>
  </v-card>
</template>
  
<script lang="ts" setup>
  import { Lesson } from '../utils/types'
  import { PropType } from 'vue'

  defineProps({
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