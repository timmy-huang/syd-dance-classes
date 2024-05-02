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
  const date = ref(new Date("Mon Apr 22 2024 18:00:00 GMT+1000 (Australian Eastern Standard Time)"))

  const displayData = computed(() => {
    // Check that the lesson is on the day we want
    if (lessons.value) {
      console.log(lessons.value[0].start)
      console.log(date.value)
      return lessons.value.filter((lesson) => 
        lesson.start.getDate() === date.value.getDate() && 
        lesson.start.getMonth() === date.value.getMonth() && 
        lesson.start.getFullYear() === date.value.getFullYear()
      )
    }
    return []
  })

  onMounted(async () => {
    // TODO give every lesson a uniq id
    const data = await getData()
    lessons.value = data.map((lesson: Lesson) => ({
      ...lesson,
      start: new Date(lesson.start),
      end: new Date(lesson.end)
    }))
    console.log("d")
    console.log(data)
    console.log(lessons.value)

  })
</script>
