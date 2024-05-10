<template>
  <v-card
    hover
    elevation="6"
  >
    <template v-slot:prepend>
      <StudioIcon :studio="lesson.studio" />
    </template> 

    <template v-slot:title>
      {{ lesson.name }}
    </template>

    <template v-slot:subtitle>
      {{ lesson.choreo }}
    </template>

    <template v-slot:text>
      {{ formatDate(lesson.start) + " - " + formatDate(lesson.end) }}
    </template>
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
</style>