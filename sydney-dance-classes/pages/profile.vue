<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>My Profile</v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
              <v-text-field
                v-model="profile.email"
                label="Email"
                disabled
              />
              
              <v-text-field
                v-model="profile.name"
                label="Name"
              />
              
              <v-text-field
                v-model="profile.phone"
                label="Phone"
              />
              
              <v-alert v-if="message" type="success" class="mt-4">
                {{ message }}
              </v-alert>
              
              <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                class="mt-4"
              >
                Update Profile
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
definePageMeta({
  middleware: 'auth' // Only logged-in users can access
})

const supabase = useSupabaseClient()
const user = useSupabaseUser()

const profile = ref({
  email: '',
  name: '',
  phone: ''
})

const loading = ref(false)
const message = ref('')
const profileLoaded = ref(false)

// Load profile when user becomes available
watchEffect(async () => {
  // Wait for user to be available and only load once
  if (!user.value?.id || profileLoaded.value) {
    return
  }
  
  profileLoaded.value = true
  loading.value = true
  
  try {
    // Initialize with user info from auth
    profile.value = {
      email: user.value.email || '',
      name: user.value.user_metadata?.name || '',
      phone: ''
    }
    
    // Load profile from database and merge with user info
    // Use maybeSingle() instead of single() to handle case where profile doesn't exist
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.value.id)
      .maybeSingle()
    
    if (error && error.code !== 'PGRST116') {
      // PGRST116 is "no rows returned" which is expected if profile doesn't exist
      console.error('Error loading profile:', error)
    }
    
    if (data) {
      console.log('data', data)
      // Merge database profile with user auth data (email from auth takes priority)
      profile.value = {
        email: user.value.email || data.email || '',
        name: data.name || user.value.user_metadata?.name || '',
        phone: data.phone || ''
      }
    }
  } catch (err) {
    console.error('Unexpected error loading profile:', err)
  } finally {
    loading.value = false
  }
})

const updateProfile = async () => {
  if (!user.value?.id) {
    alert('User not authenticated')
    return
  }
  
  loading.value = true
  message.value = ''
  
  const { error } = await supabase
    .from('profiles')
    .update({
      name: profile.value.name,
      phone: profile.value.phone,
      updated_at: new Date().toISOString()
    })
    .eq('id', user.value.id)
  
  if (error) {
    alert('Error updating profile')
  } else {
    message.value = 'Profile updated successfully!'
  }
  
  loading.value = false
}
</script>