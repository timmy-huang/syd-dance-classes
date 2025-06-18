<template>
  <div class="d-flex flex-column align-center">
    <v-row>
      <v-col
        v-for="event in events"
        :key="event.id"
        cols="12"
        sm="6"
        md="4"
      >
        <div class="pa-2">
          <EventCard :event="event" />
        </div>
      </v-col>
    </v-row>
    
    <!-- Big Plus Button -->
    <v-btn
      class="mt-6 mb-4"
      size="x-large"
      color="primary"
      icon
      elevation="4"
      @click="handleAddEvent"
    >
      <v-icon size="48">mdi-plus</v-icon>
    </v-btn>
    
    <NoClassesFound 
      v-if="events.length === 0"
      message="No upcoming events at this time."
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import EventCard from './EventCard.vue'
import NoClassesFound from './NoClassesFound.vue'
import { fetchSheetData } from '../utils/googleSheets'

// Events data and state
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

const fetchEvents = async () => {
  try {
    const SPREADSHEET_ID = '13LyToNV0c_1UR_nJQfC2ShdYuSDJeddIvMVdO9JQZVg'
    const SHEET_NAME = 'Events'

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

const handleAddEvent = () => {
  console.log('Add event button clicked')
  // Open the Google Form in a new tab
  window.open('https://docs.google.com/forms/d/e/1FAIpQLSdnd9xh8RE12faM62DgWTADUPXkyBa-gLnWkIW2gTfIsedbrg/viewform', '_blank')
}

// Fetch events when component is mounted
onMounted(() => {
  fetchEvents()
})

// Expose fetchEvents for parent component to call
defineExpose({
  fetchEvents
})
</script> 