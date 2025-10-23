<template>
  <div class="d-flex flex-column align-center">
    <FilterBox 
      :beg="beg"
      :inte="inte"
      :adv="adv"
      :popUp="popUp"
      :search="search"
      :selectedStudios="selectedStudios"
      :selectedStyles="selectedStyles"
      @update:beg="toggleBeg"
      @update:inte="toggleInte"
      @update:adv="toggleAdv"
      @update:popUp="togglePopUp"
      @update:search="search = $event.target.value"
      @update:selectedStudios="updateSelectedStudios"
      @update:selectedStyles="updateSelectedStyles"
    />
    <Calendar 
      :selectedDate="selectedDate"
      :mondayDate="mondayDate"
      @update="handleUpdateDate"
    />
  </div>
  <div class="mt-5">
    <LessonCard
      v-for="(lesson, index) in displayData"
      :key="`${lesson.serviceId}-${index}`"
      :lesson="lesson"
    />
    <NoClassesFound 
      v-if="displayData.length === 0"
      :message="getNoClassesMessage()"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, Ref } from 'vue'
import FilterBox from './FilterBox.vue'
import Calendar from './Calendar.vue'
import LessonCard from './LessonCard.vue'
import NoClassesFound from './NoClassesFound.vue'
import { Lesson } from '../utils/types'
import { studios, styles } from '../utils/consts'

// Props
interface Props {
  lessons: Lesson[]
}

const props = defineProps<Props>()

// Classes data and state
const search = ref<string>('')
const beg = ref(localStorage.getItem('beg') ? JSON.parse(localStorage.getItem('beg')!) : true)
const inte = ref(localStorage.getItem('inte') ? JSON.parse(localStorage.getItem('inte')!) : true)
const adv = ref(localStorage.getItem('adv') ? JSON.parse(localStorage.getItem('adv')!) : true)  
const popUp = ref(localStorage.getItem('popUp') ? JSON.parse(localStorage.getItem('popUp')!) : true)

const selectedStudios = ref(localStorage.getItem('selectedStudios') ? JSON.parse(localStorage.getItem('selectedStudios')!) : [...studios])
const selectedStyles = ref(localStorage.getItem('selectedStyles') ? JSON.parse(localStorage.getItem('selectedStyles')!) : [...styles])

// Handle the selected day
const today = ref(new Date())
const selectedDate = ref(today.value)
const mondayDate = new Date(new Date(today.value.valueOf()).setDate(today.value.getDate() - (today.value.getDay() + 6) % 7))

const displayData = computed(() => {
  console.log('displayData')
  if (!props.lessons) {
    console.log('No lessons')
    return []
  }
  
  const temp = props.lessons.filter((lesson) => {  // filter lessons by day
    return lesson.start.getDate() === selectedDate.value.getDate() && 
    lesson.start.getMonth() === selectedDate.value.getMonth() && 
    lesson.start.getFullYear() === selectedDate.value.getFullYear()
  }).filter((lesson) => {  // filter lessons by search (name, studio, choreo)
    return lesson.name.toLowerCase().includes(search.value.toLowerCase()) || 
    lesson.studio.toLowerCase().includes(search.value.toLowerCase()) || 
    lesson.choreo.name.toLowerCase().includes(search.value.toLowerCase())
  }).filter((lesson) => {  // filter lessons by level
    return (beg.value && lesson.level.includes('beginner')) || 
    (inte.value && lesson.level.includes('intermediate')) ||
    (adv.value && lesson.level.includes('advanced')) ||
    (popUp.value && lesson.level.includes('pop-up'))
  }).filter((lesson) => {  // filter lessons by studio
    return selectedStudios.value.includes(lesson.studio)
  }).filter((lesson) => { // Filter by style
    return selectedStyles.value.some(style => lesson.style.includes(style))
  }).sort((a, b) => {  // sort lessons by start time
    return a.start.getTime() - b.start.getTime()
  })
  
  return temp
})

const handleUpdateDate = (newDate: Date) => {
  selectedDate.value = newDate
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

const togglePopUp = () => {
  popUp.value = !popUp.value
  localStorage.setItem('popUp', JSON.stringify(popUp.value))
}

const getNoClassesMessage = () => {
  if (!props.lessons || props.lessons.length === 0) {
    return 'Loading classes data...'
  }
  
  // Check if any filters are applied
  const hasFilters = search.value || 
                    !beg.value || 
                    !inte.value || 
                    !adv.value || 
                    !popUp.value ||
                    selectedStudios.value.length < studios.length ||
                    selectedStyles.value.length < styles.length;
                    
  if (hasFilters) {
    return 'No classes match your current filters. Try adjusting your search criteria.'
  }
  
  return `No classes found for ${selectedDate.value.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}.`
}
</script> 