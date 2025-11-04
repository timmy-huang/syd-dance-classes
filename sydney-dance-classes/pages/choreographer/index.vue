<template>
  <v-container>
    <h1 class="text-h4 mb-6">Choreographers</h1>
    
    <v-row>
      <v-col
        v-for="choreo in choreographers"
        :key="choreo.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card>
          <v-img
            :src="choreo.profile_image_url || 'https://via.placeholder.com/400x300?text=No+Image'"
            height="200"
            cover
          />
          
          <v-card-title>{{ choreo.name }}</v-card-title>
          
          <v-card-text>
            <div v-if="choreo.instagram" class="mb-2">
              <v-icon size="small">mdi-instagram</v-icon>
              {{ choreo.instagram }}
            </div>
            
            <div v-if="choreo.bio" class="text-body-2">
              {{ choreo.bio.slice(0, 100) }}{{ choreo.bio.length > 100 ? '...' : '' }}
            </div>
            
            <v-chip
              v-if="choreo.is_independent"
              color="primary"
              size="small"
              class="mt-2"
            >
              Hosts Classes
            </v-chip>
          </v-card-text>
          
          <v-card-actions>
            <v-btn
              :to="`/choreographers/${choreo.id}`"
              variant="text"
              color="primary"
            >
              View Profile
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <div v-if="choreographers.length === 0" class="text-center py-8">
      <v-icon size="64" color="grey">mdi-account-search</v-icon>
      <p class="text-h6 mt-4">No choreographers yet</p>
    </div>
  </v-container>
</template>

<script setup>
const supabase = useSupabaseClient()

const { data: choreographers } = await useAsyncData('choreographers', async () => {
  const { data } = await supabase
    .from('choreographers')
    .select('*')
    .order('name')
  
  return data || []
})
</script>