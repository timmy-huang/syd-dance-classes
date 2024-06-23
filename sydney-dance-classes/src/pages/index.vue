<template>
  <v-responsive
    class="align-centerfill-height mx-auto"
    max-width="900"
  >
    <Calendar 
      :selectedDay="day"
      @update="handleUpdateDay"
      class="mt-10"
    />
    <div>
      <LessonCard
        v-for="lesson in displayData"
        :key="lesson.serviceId"
        :lesson="lesson"
      />
    </div>
    
  </v-responsive>
  
</template>

<script lang="ts" setup>
  // Get the classes from data
  import { computed, onMounted, ref, Ref, toRaw } from 'vue'
  import getData from '../utils/data'
  import LessonCard from '../components/LessonCard.vue';
  import { Lesson } from '../utils/types'

  const lessons: Ref<Lesson[]> = ref([]);
  
  const today = ref(new Date())
  console.log(today)
  const day = ref((today.value.getDay()+ 6) % 7);// 0 = Monday

  const selectedDate = computed(() => {
    var date = new Date(today.value.valueOf());
    date.setDate(date.getDate() + day.value);
    return date;
  });

  const displayData = computed(() => {
    if (lessons.value) {
      if (lessons.value.length > 0) {
        const temp = lessons.value.filter((lesson) => {
          return lesson.start.getDate() === selectedDate.value.getDate() && 
          lesson.start.getMonth() === selectedDate.value.getMonth() && 
          lesson.start.getFullYear() === selectedDate.value.getFullYear()
        }).sort((a, b) => {
          return a.start.getTime() - b.start.getTime()
        })
        return temp
      } 
    }
    console.log('No lessons')
    return []
  })

  const handleUpdateDay = (newDay: number) => {
    day.value = newDay
  }

  onMounted(async () => {
    // TODO give every lesson a uniq id
    await getData(lessons)
    console.log(lessons.value)
  })
</script>
