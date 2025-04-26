<template>
  <v-card
    hover
    elevation="6"
    class="d-flex align-center"
    v-if="$vuetify.display.mdAndUp"
  >

    <v-card-item class="lesson-card-item">
      <template v-slot:prepend>
        <StudioIcon :studio="lesson.studio" />
      </template> 
      <v-card-title>
        {{ lesson.name }}
      </v-card-title>
      <v-card-subtitle>
        <router-link 
          :to="`/choreographer/${lesson.choreo.id}`"
          class="choreo-link"
        >
          {{ lesson.choreo.name }}
        </router-link>
        <v-btn
          icon="mdi-instagram"
          size="small"
          variant="text"
          :href="`https://www.instagram.com/${lesson.choreo.instagram.replace('@', '')}`"
          target="_blank"
          rel="noopener"
          class="ml-1"
          v-if="lesson.choreo.instagram"
        >
        </v-btn>
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <div class="d-flex-column align-center">
        <div v-if="displayDay">
          {{ lesson.start.toLocaleDateString('en-US', { weekday: 'long' }) }}
        </div>
        <div class="text-subtitle-1">
          {{ formatDate(lesson.start) + " - " + formatDate(lesson.end) }}
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        variant="outlined"
        class="mr-4"
        :href="bookLink"
        target="_blank"
        rel="noopener"
      >
        Book Now
      </v-btn>
    </v-card-actions>
  </v-card>

  <v-card
    hover
    elevation="6"
    class="d-flex align-center"
    v-else
    link
    :href="bookLink"
    target="_blank"
    rel="noopener"
  >
    <v-card-item class="lesson-card-item-mobile">
      <v-card-title class="text-wrap">
        {{ lesson.name }}
      </v-card-title>
      <v-card-subtitle>
        <router-link 
          :to="`/choreographer/${lesson.choreo.id}`"
          class="choreo-link"
        >
          {{ lesson.choreo.name }}
        </router-link>
        <v-btn
          icon="mdi-instagram"
          size="small"
          variant="text"
          :href="`https://www.instagram.com/${lesson.choreo.instagram.replace('@', '')}`"
          target="_blank"
          rel="noopener"
          class="ml-1"
          v-if="lesson.choreo.instagram"
          @click.stop
        >
        </v-btn>
      </v-card-subtitle>
      <v-card-text class="px-0 d-flex align-center justify-space-between">
        <studio-icon :studio="lesson.studio" />
        <div class="d-flex-column align-center">
          <div v-if="displayDay">
            {{ lesson.start.toLocaleDateString('en-US', { weekday: 'long' }) }}
          </div>
          <div class="text-subtitle-1">
            {{ formatDate(lesson.start) + " - " + formatDate(lesson.end) }}
          </div>
        </div>
      </v-card-text>
    </v-card-item>
  </v-card>
</template>
  
<script lang="ts" setup>
  import { Lesson } from '../utils/types'
  import { PropType } from 'vue'
  import { computed } from 'vue'
  import { useDisplay } from 'vuetify'

  const bookLink = computed(() => {
    if (props.lesson) {
      if (props.lesson.studio === "Movement Nation Hurstville") {
        return "https://www.movementnation.com.au/hurstville-bookings"
      }
      if (props.lesson.studio === "Movement Nation Parramatta") {
        return "https://2020movementnation.wixsite.com/website-1"
      }
      if (props.lesson.studio === "IMI") {
        return "https://imient.com.au/classes"
      }
      if (props.lesson.studio === "Crossover") {
        return "https://www.crossoverdance.com/timetable/"
      }
      if (props.lesson.studio === "IX") {
        return "https://www.ixdancestudio.com/booking"
      }
      if (props.lesson.studio === "PDC") {
        return "https://www.pdcdance.net/book-online"
      }
      if (props.lesson.studio === "DUTI") {
        return "https://www.dutistudios.com.au/timetable"
      }
      if (props.lesson.studio === "Endless") {
        return "https://www.endlessdance.com.au/classes"
      }
    }
    console.log("Booking Link not found for ", props.lesson)
    return ""
  })

  const props = defineProps({
    lesson: Object as PropType<Lesson>,
    displayDay: {
      type: Boolean,
      default: false
    }
  })

  const formatDate = (date: Date) => {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true }).replace(" ", "")
  }
</script>

<style>
  .v-card {
    margin: 1em;
  }

  .lesson-card-item {
    width: 500px;
  }

  .lesson-card-item-mobile {
    width: 100%;
  }

  .choreo-link {
    text-decoration: none;
    color: inherit;
  }

  .choreo-link:hover {
    text-decoration: underline;
  }
</style>