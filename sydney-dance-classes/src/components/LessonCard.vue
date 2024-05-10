<template>
  <v-card>
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
      {{ lesson.start }}
    </template>
    </v-card>
</template>
  
<script lang="ts" setup>
  import { Lesson } from '../utils/types'
  import { PropType } from 'vue'

  defineProps({
    lesson: Object as PropType<Lesson>,
  })
</script>