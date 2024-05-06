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
  import { computed, onMounted, ref, Ref, toRaw } from 'vue'
  import getData from '../utils/data'
  import LessonCard from '../components/LessonCard.vue';
  import { Lesson } from '../utils/types'

  const lessons: Ref<Lesson[]> = ref([]);
  const day = ref('Monday')
  const date = ref(new Date("Mon Apr 29 2024 18:00:00 GMT+1000 (Australian Eastern Standard Time)"))

  const displayData = computed(() => {
    // Check that the lesson is on the day we want
    // console.log("test")
    if (lessons.value) {
      console.log("lessons")
      // console.log(lessons.value)
      // console.log(lessons.value[0])
      if (lessons.value.length > 0) {
        console.log("filtering lessons")
        const temp = lessons.value.filter((lesson) => {
          return lesson.start.getDate() === date.value.getDate() && 
          lesson.start.getMonth() === date.value.getMonth() && 
          lesson.start.getFullYear() === date.value.getFullYear()
      })
        return temp
      } 
    }
    console.log('No lessons')
    return []
  })

  onMounted(async () => {
    // TODO give every lesson a uniq id
    await getData(lessons)
    console.log(lessons.value)
  })
</script>
