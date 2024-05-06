<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >
      <Calendar />
      <LessonCard
        v-for="lesson in displayData"
        :key="lesson.serviceId"
        :title="lesson.name"
        :subtitle="lesson.choreo"
        :text="lesson.start"
      />
    </v-responsive>
  </v-container>
  
</template>

<script lang="ts" setup>
  // Get the classes from data
  import { computed, onMounted, ref, Ref } from 'vue'
  import getData from '../utils/data'
  import LessonCard from '../components/LessonCard.vue';
  import { Lesson } from '../utils/types'

  const lessons: Ref<Lesson[] | null> = ref(null);
  const day = ref('Monday')
  const date = ref(new Date("Mon Apr 29 2024 18:00:00 GMT+1000 (Australian Eastern Standard Time)"))

  const displayData = computed(() => {
    // Check that the lesson is on the day we want
    if (lessons.value) {
      if (lessons.value.length > 0) {
        console.log("filtering lessons")
        const temp = lessons.value.filter((lesson) => {
          console.log(lesson.start)
          console.log(date.value)
          return lesson.start.getDate() === date.value.getDate() && 
          lesson.start.getMonth() === date.value.getMonth() && 
          lesson.start.getFullYear() === date.value.getFullYear()
      })
        console.log(temp)
        console.log(date.value)
        console.log(lessons.value)
        console.log(lessons.value[0])
        return temp
      } 
    }
    console.log('No lessons')
    return []
  })

  onMounted(async () => {
    // TODO give every lesson a uniq id
    lessons.value = await getData()
    console.log(lessons.value)
  })
</script>
