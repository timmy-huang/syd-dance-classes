<template>
  <v-responsive
    class="align-center fill-height mx-auto"
    max-width="975"
  >
    <div style="justify-content: center; align-items: center;" class="mt-2 d-flex flex-column">      
      <!-- Tabs for switching between Classes and Events -->
      <!-- <ClientOnly>
        <v-tabs
          v-model="activeTab"
          color="primary"
          class="mb-6"
          centered
          :touch="false"
          height="60"
        >
          <v-tab value="classes" :size="tabSize">Classes</v-tab>
          <v-tab value="events" :size="tabSize">Events</v-tab>
        </v-tabs>
      </ClientOnly> -->
      <!-- Tab Content -->
      <!-- <v-window v-model="activeTab" :touch="false">
        <v-window-item value="classes">
          <Classes :lessons="lessonsValue" />
        </v-window-item>

        <v-window-item value="events">
          <Events />
        </v-window-item>
      </v-window> -->
    </div>
  </v-responsive>
</template>

<script lang="ts" setup>
  // Get the classes from data
  // import getData from '../utils/data'
  // import Classes from '../components/Classes.vue'
  //import Events from '../components/Events.vue'


  // Tab management
  const activeTab = ref('classes')

  // Responsive tab size
  const tabSize = computed(() => {
    // Getting server side rendering issues with this
    return 'large'
    //return display.smAndDown.value ? 'large' : 'x-large'
  })

  // Classes data and state
  const lessons = ref<Lesson[]>([])

  // Computed property to pass lessons value
  const lessonsValue = computed(() => lessons.value)

  onMounted(async () => {
    // Load classes data
    //await getData(lessons)
    //console.log(lessons.value)
  })
</script>

<style scoped>
.event-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.v-card-actions {
  margin-top: auto;
  padding: 16px;
}
</style> 