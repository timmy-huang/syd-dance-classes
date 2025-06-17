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
        <EventCard :event="event" />
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
import EventCard from '../components/EventCard.vue'
import { fetchSheetData } from '../utils/googleSheets'

interface Event {
  id: string
  title: string
  date: Date
  location: string
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
    const SPREADSHEET_ID = '13LyToNV0c_1UR_nJQfC2ShdYuSDJeddIvMVdO9JQZVg'
    const SHEET_NAME = 'Events' // Update this to match your sheet name

    const rows = await fetchSheetData(SPREADSHEET_ID, SHEET_NAME)
    console.log('Raw data:', rows)
    
    if (!rows || rows.length < 1) {
      console.warn('No events found or invalid data format')
      events.value = []
      return
    }

    const now = new Date()
    
    // Map the data to events and filter out past events
    events.value = rows
      .map((row: any[]): Event => ({
        id: String(row[0] || ''), // Date
        title: String(row[1] || ''), // Title
        date: row[2] instanceof Date ? row[2] : new Date(row[2] || ''), // Event Date
        location: String(row[3] || ''), // Location
        description: String(row[4] || ''), // Description
        image: String(row[5] || ''), // Image URL
        link: String(row[6] || '') // Event Link
      }))
      .filter(event => event.date >= now)
      .sort((a, b) => a.date.getTime() - b.date.getTime()) // Sort by date ascending
    
    console.log('Processed events:', events.value)
  } catch (error) {
    console.error('Error fetching events:', error)
    events.value = [] // Clear events on error
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
