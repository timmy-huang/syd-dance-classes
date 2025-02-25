<template>
  <v-responsive
    class="align-centerfill-height mx-auto"
    max-width="900"
  >
    <div style="justify-content: center; align-items: center;" class="mt-10 d-flex flex-column">
      <div class="text-h2 my-7 text-center">
        Class Schedule
      </div>
      <FilterBox 
        :beg="beg"
        :inte="inte"
        :adv="adv"
        :search="search"
        :selectedStudios="selectedStudios"
        :selectedStyles="selectedStyles"
        @update:beg="toggleBeg"
        @update:inte="toggleInte"
        @update:adv="toggleAdv"
        @update:search="search = $event.target.value"
        @update:selectedStudios="updateSelectedStudios"
        @update:selectedStyles="updateSelectedStyles"
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
  import { Lesson } from '../utils/types'
  import { studios, styles } from '../utils/consts';

  const lessons: Ref<Lesson[]> = ref([]);

  const search = ref<string>('')
  const beg = ref(localStorage.getItem('beg') ? JSON.parse(localStorage.getItem('beg')!) : true)
  const inte = ref(localStorage.getItem('inte') ? JSON.parse(localStorage.getItem('inte')!) : true)
  const adv = ref(localStorage.getItem('adv') ? JSON.parse(localStorage.getItem('adv')!) : true)  

  const selectedStudios = ref(localStorage.getItem('selectedStudios') ? JSON.parse(localStorage.getItem('selectedStudios')!) : [...studios])
  const selectedStyles = ref(localStorage.getItem('selectedStyles') ? JSON.parse(localStorage.getItem('selectedStyles')!) : [...styles])

  // Handle the selected day
  const today = ref(new Date())

  // If Sunday, show from Monday. In future it should be, if day is empty, show next day
  // Also in the future should show next week
  if (today.value.getDay() === 0) { 
    today.value.setDate(today.value.getDate() + 1);
  }
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
    }).filter((lesson) => {  // filter lessons by studio
      return selectedStudios.value.includes(lesson.studio)
    }).filter((lesson) => { // Filter by style
      return selectedStyles.value.some(style => lesson.style.includes(style))
    }).sort((a, b) => {  // sort lessons by start time
      return a.start.getTime() - b.start.getTime()
    })
    
    return temp
  })

  const handleUpdateDay = (newDay: number) => {
    day.value = newDay
  }

  const updateSelectedStudios = (newStudios: string[]) => {
    selectedStudios.value = newStudios
    localStorage.setItem('selectedStudios', JSON.stringify(selectedStudios.value))
  }

  const updateSelectedStyles = (newStyles: string[]) => {
    selectedStyles.value = newStyles
    localStorage.setItem('selectedStyles', JSON.stringify(selectedStyles.value))
  }

  const toggleBeg = () => {
    beg.value = !beg.value
    localStorage.setItem('beg', JSON.stringify(beg.value))
  }

  const toggleInte = () => {
    inte.value = !inte.value
    localStorage.setItem('inte', JSON.stringify(inte.value))
  }

  const toggleAdv = () => {
    adv.value = !adv.value
    localStorage.setItem('adv', JSON.stringify(adv.value))
  }

  onMounted(async () => {
    // TODO give every lesson a uniq id
    await getData(lessons)
    console.log(lessons.value)
  })
</script>
