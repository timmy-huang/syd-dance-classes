<template>
  <v-responsive
    class="mx-auto"
    max-width="900"
  >
    <div class="mt-5 ml-2">
      <v-btn
        prepend-icon="mdi-arrow-left"
        variant="text"
        @click="goBack"
      >
        Back
      </v-btn>
    </div>
    <div style="justify-content: center; align-items: center;" class="mt-5 d-flex flex-column">
      <div class="text-h2 my-7 text-center" v-if="choreographer">
        {{ choreographer.name }}'s Classes
        <v-btn
          icon="mdi-instagram"
          size="large"
          variant="text"
          :href="`https://www.instagram.com/${choreographer.instagram.replace('@', '')}`"
          target="_blank"
          rel="noopener"
          class="ml-1"
          v-if="choreographer.instagram"
        >
        </v-btn>
      </div>
      <div v-else class="text-h4 my-7">
        Loading choreographer data...
      </div>
    </div>
    <div>
      <div v-if="displayData.length === 0" class="text-center my-5">
        No classes found for this choreographer.
      </div>
      <LessonCard
        v-for="(lesson, index) in displayData"
        :key="`${lesson.serviceId}-${index}`"
        :lesson="lesson"
        :displayDay="true"
      />
    </div>
  </v-responsive>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, Ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import getData from '../../utils/data'
import { Lesson, Choreographer } from '../../utils/types'

const route = useRoute()
const router = useRouter()
const choreographerId = computed(() => route.params.id as string)
console.log('Route params:', route.params)
console.log('Choreographer ID:', choreographerId.value)

const lessons: Ref<Lesson[]> = ref([])
const choreographer = ref<Choreographer | null>(null)

const goBack = () => {
  router.go(-1)
}

const displayData = computed(() => {
  console.log('Display Data - Lessons count:', lessons.value.length)
  if (!lessons.value.length) {
    return []
  }
  
  const filtered = lessons.value
    .filter(lesson => {
      return lesson.choreo.id === choreographerId.value
    })
  console.log('Filtered Lessons count:', filtered.length)
  return filtered.sort((a, b) => a.start.getTime() - b.start.getTime())
})

const fetchData = async () => {
  console.log('Fetching data for choreographer:', choreographerId.value)
  await getData(lessons)
  console.log('Data fetched, lessons count:', lessons.value.length)
  
  // Find choreographer details
  if (lessons.value.length > 0) {
    const firstLesson = lessons.value.find(lesson => lesson.choreo.id === choreographerId.value)
    console.log('First matching lesson:', firstLesson)
    if (firstLesson) {
      choreographer.value = firstLesson.choreo
      console.log('Found choreographer:', choreographer.value)
    } else {
      console.log('No matching lesson found for choreographer ID:', choreographerId.value)
    }
  }
}

onMounted(fetchData)

// Re-fetch data if the route param changes
watch(choreographerId, fetchData)
</script>
