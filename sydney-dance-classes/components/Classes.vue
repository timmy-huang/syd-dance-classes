<template>
  <div class="d-flex flex-column align-center">
    <FilterBox 
      :youth="youth"
      :beg="beg"
      :inte="inte"
      :adv="adv"
      :popUp="popUp"
      :search="search"
      :selectedStudios="selectedStudios"
      :selectedStyles="selectedStyles"
      @update:youth="toggleYouth"
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
import type { Lesson } from '~/types';
import { studios, styles } from '~/utils/consts';

// Helper function to safely get from localStorage (only on client)
const getFromLocalStorage = (key: string, defaultValue: any) => {
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    const item = localStorage.getItem(key)
    if (item) {
      try {
        return JSON.parse(item)
      } catch (e) {
        return defaultValue
      }
    }
  }
  return defaultValue
}

// Props
interface Props {
  lessons: Lesson[]
}

const props = defineProps<Props>()

// Classes data and state
const search = ref<string>('')
const youth = ref(false)
const beg = ref(true)
const inte = ref(true)
const adv = ref(true)  
const popUp = ref(true)

const selectedStudios = ref<string[]>([])
const selectedStyles = ref<string[]>([])

// Load from localStorage on client side
onMounted(() => {
  youth.value = getFromLocalStorage('youth', false)
  beg.value = getFromLocalStorage('beg', true)
  inte.value = getFromLocalStorage('inte', true)
  adv.value = getFromLocalStorage('adv', true)
  popUp.value = getFromLocalStorage('popUp', true)
  
  const savedStudios = getFromLocalStorage('selectedStudios', null)
  const savedStyles = getFromLocalStorage('selectedStyles', null)
  
  selectedStudios.value = savedStudios || [...studios]
  selectedStyles.value = savedStyles || [...styles]
})

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
    return (
      (beg.value && lesson.level.includes('beginner')) || 
      (inte.value && lesson.level.includes('intermediate')) ||
      (adv.value && lesson.level.includes('advanced')) ||
      (popUp.value && lesson.level.includes('pop-up')) ||
      (youth.value && lesson.level.includes('youth'))
    )
  }).filter((lesson) => {  // filter lessons by studio
    return selectedStudios.value.includes(lesson.studio)
  }).filter((lesson) => { // Filter by style
    return selectedStyles.value.some((style: string) => lesson.style.includes(style))
  }).sort((a, b) => {  // sort lessons by start time then end time
    if (a.start.getTime() === b.start.getTime()) {
      return a.end.getTime() - b.end.getTime()
    }
    return a.start.getTime() - b.start.getTime()
  })
  
  return temp
})

const handleUpdateDate = (newDate: Date) => {
  selectedDate.value = newDate
}

const updateSelectedStudios = (newStudios: string[]) => {
  selectedStudios.value = newStudios
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('selectedStudios', JSON.stringify(selectedStudios.value))
  }
}

const updateSelectedStyles = (newStyles: string[]) => {
  selectedStyles.value = newStyles
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('selectedStyles', JSON.stringify(selectedStyles.value))
  }
}

const toggleYouth = () => {
  youth.value = !youth.value
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('youth', JSON.stringify(youth.value))
  }
}

const toggleBeg = () => {
  beg.value = !beg.value
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('beg', JSON.stringify(beg.value))
  }
}

const toggleInte = () => {
  inte.value = !inte.value
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('inte', JSON.stringify(inte.value))
  }
}

const toggleAdv = () => {
  adv.value = !adv.value
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('adv', JSON.stringify(adv.value))
  }
}

const togglePopUp = () => {
  popUp.value = !popUp.value
  if (import.meta.client && typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('popUp', JSON.stringify(popUp.value))
  }
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