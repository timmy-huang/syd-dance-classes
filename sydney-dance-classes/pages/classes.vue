<template>
  <v-responsive
    class="mx-auto"
    max-width="975"
  >
    <div>
      <div style="justify-content: center; align-items: center;" class="mt-2 d-flex flex-column">      
        <Classes :lessons="lessonsValue" />
      </div>
    </div>
  </v-responsive>
</template>

<script lang="ts" setup>
  // Get the classes from data
  import getData from '../utils/data'
  import Classes from '../components/Classes.vue'

  // Classes data and state
  const lessons = ref<Lesson[]>([])

  // Computed property to pass lessons value
  const lessonsValue = computed(() => lessons.value)

  onMounted(async () => {
    // Load classes data
    await getData(lessons)
    console.log(lessons.value)
  })
</script>

