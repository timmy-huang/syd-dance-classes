<template>
  <v-responsive
    class="align-centerfill-height mx-auto"
    max-width="900"
  >
    <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;" class="mt-10;">
      <div class="text-h2 my-7">
        Class Schedule
      </div>
      <FilterBox 
        :beg="beg"
        :inte="inte"
        :adv="adv"
        :search="search"
        @update:beg="beg = !beg"
        @update:inte="inte = !inte"
        @update:adv="adv = !adv"
        @update:search="search = $event.target.value"
      />
      <Calendar 
        :selectedDay="day"
        :mondayDate="mondayDate"
        @update="handleUpdateDay"
      />
    </div>
    <div>
      <LessonCard
        v-for="(lesson, index) in displayData"
        :key="`${lesson.serviceId}-${index}`"
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
  import { Lesson, SelectedStudio } from '../utils/types'

  const lessons: Ref<Lesson[]> = ref([]);

  const search = ref<string>('')
  const beg = ref(true)
  const inte = ref(true)
  const adv = ref(true)
  
  const selectedStudios = ref([
    {name: 'Movement Nation Hurstville', selected: true},
    {name: 'Dancekool', selected: true},
    {name: 'Latin Dance Australia', selected: true},
    {name: 'Salsa Republic', selected: true},
    {name: 'Salsabor', selected: true},
    {name: 'Salsa Suave', selected: true},
    {name: 'Salsa Synergy', selected: true},
    {name: 'Salsa Vida', selected: true}
  ])

  // Handle the selected day
  const today = ref(new Date())

  // If Sunday, show from Monday. In future it should be, if day is empty, show next day
  // Also in the future should show next week
  if (today.value.getDay() === 0) { 
    today.value.setDate(today.value.getDate() + 1);
  }
  // console.log(today.value)
  const day = ref((today.value.getDay()+ 6) % 7);// 0 = Monday

  const mondayDate = new Date(new Date(today.value.valueOf()).setDate(today.value.getDate() - day.value));

  const selectedDate = computed(() => {
    var date = new Date(mondayDate.valueOf());
    date.setDate(date.getDate() + day.value);
    return date;
  });

  const displayData = computed(() => {
    console.log('displayData')
    if (!lessons.value) {
      console.log('No lessons')
      return []
    }

    
    console.log(search.value)
    const temp = lessons.value.filter((lesson) => {  // filter lessons by day
      return lesson.start.getDate() === selectedDate.value.getDate() && 
      lesson.start.getMonth() === selectedDate.value.getMonth() && 
      lesson.start.getFullYear() === selectedDate.value.getFullYear()
    }).filter((lesson) => {  // filter lessons by search (name, studio, choreo)
      return lesson.name.toLowerCase().includes(search.value.toLowerCase()) || 
      lesson.studio.toLowerCase().includes(search.value.toLowerCase()) || 
      lesson.choreo.toLowerCase().includes(search.value.toLowerCase())
    }).filter((lesson) => {  // filter lessons by level
      return (beg.value && lesson.level.includes('beginner')) || 
      (inte.value && lesson.level.includes('intermediate')) ||
      (adv.value && lesson.level.includes('advanced'))
    }).sort((a, b) => {
      return a.start.getTime() - b.start.getTime()
    })
    
    return temp
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
