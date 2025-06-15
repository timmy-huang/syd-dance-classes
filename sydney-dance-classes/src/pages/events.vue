<template>
  <v-responsive
    class="mx-auto"
    max-width="900"
  >
    <div style="justify-content: center; align-items: center;" class="mt-10 d-flex flex-column">
      <div class="text-h2 my-7 text-center">
        Events
      </div>
    </div>

    <v-row>
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mx-auto event-card">
          <v-img
            :src="event.image"
            height="200px"
            cover
          ></v-img>

          <v-card-title>{{ event.title }}</v-card-title>

          <v-card-subtitle>
            {{ formatDate(event.date) }}
          </v-card-subtitle>

          <v-card-text>
            {{ event.description }}
          </v-card-text>

          <v-card-actions>
            <v-btn
              variant="outlined"
              :href="event.link"
              target="_blank"
              rel="noopener"
            >
              Learn More
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <NoClassesFound 
      v-if="events.length === 0"
      message="No upcoming events at this time."
    />
  </v-responsive>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import NoClassesFound from '../components/NoClassesFound.vue'

interface Event {
  id: string
  title: string
  date: Date
  description: string
  image: string
  link: string
}

const events = ref<Event[]>([])

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const fetchEvents = async () => {
  try {
    // Replace with your Google Sheets API endpoint
    const response = await fetch('YOUR_GOOGLE_SHEETS_API_ENDPOINT')
    const data = await response.json()
    
    events.value = data.map((event: any) => ({
      id: event.id,
      title: event.title,
      date: new Date(event.date),
      description: event.description,
      image: event.image,
      link: event.link
    }))
  } catch (error) {
    console.error('Error fetching events:', error)
  }
}

onMounted(() => {
  fetchEvents()
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
