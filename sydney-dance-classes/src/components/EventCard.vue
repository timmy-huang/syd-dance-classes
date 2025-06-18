<template>
  <v-card class="mx-auto event-card ma-2" elevation="6">
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
      <div class="location mb-2">
        <v-icon icon="mdi-map-marker" class="mr-1"></v-icon>
        {{ event.location }}
      </div>
      <div class="text-body-1">{{ event.description }}</div>
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
</template>

<script lang="ts" setup>
interface Event {
  id: string
  title: string
  date: Date
  location: string
  description: string
  image: string
  link: string
}

defineProps<{
  event: Event
}>()

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  })
}
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

.text-body-1 {
  white-space: pre-line;
}

.location {
  display: flex;
  align-items: center;
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.875rem;
}
</style> 