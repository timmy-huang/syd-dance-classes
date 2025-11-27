<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>My Profile</v-card-title>
          
          <v-card-text>
            <!-- Debug info -->
            <v-alert v-if="debug" type="info" class="mb-4">
              <pre>{{ debug }}</pre>
            </v-alert>

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
              
              <v-alert v-if="error" type="error" class="mt-4">
                {{ error }}
              </v-alert>
              
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


<script setup lang="ts">
  definePageMeta({
    middleware: 'auth'
  })

  interface Profile {
    id: string
    email: string | null
    name: string | null
    phone: string | null
    created_at?: string
    updated_at?: string
  }

  const supabase = useSupabaseClient()
  const user = useSupabaseUser()

  const profile = ref({
    email: '',
    name: '',
    phone: ''
  })

  const loading = ref(false)
  const message = ref('')
  const error = ref('')
  const debug = ref('')

  const loadProfile = async () => {
    console.log('Loading profile')
    console.log('User:', user.value)

    if (!user.value?.sub) {
      debug.value = 'No user ID found'
      console.log('No user ID')
      return
    }
    
    // debug.value = `Loading profile for user: ${user.value.sub}`
    loading.value = true
    
    try {
      const { data, error: fetchError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.value.sub)
        .single()
      
      console.log('Profile fetch result:', { data, error: fetchError })
      
      if (fetchError) {
        console.error('Error loading profile:', fetchError)
        error.value = `Error loading profile: ${fetchError.message}`
        debug.value = JSON.stringify(fetchError, null, 2)
        return
      }
      
      if (data) {
        console.log('Setting profile data:', data)
        const profileData = data as Profile
        
        profile.value = {
          email: profileData.email || user.value.email || '',
          name: profileData.name || '',
          phone: profileData.phone || ''
        }
        // debug.value = `Profile loaded successfully: ${JSON.stringify(profile.value, null, 2)}`
      } else {
        debug.value = 'No profile data returned'
      }
    } catch (err) {
      console.error('Unexpected error:', err)
      error.value = 'Unexpected error loading profile'
      debug.value = JSON.stringify(err, null, 2)
    } finally {
      loading.value = false
    }
  }

   // Watch for user to become available
  watch(user, async (newUser) => {
    if (newUser?.sub) {
      await loadProfile()
    }
  }, { immediate: true })

  const updateProfile = async () => {
    if (!user.value?.sub) {
      error.value = 'User not authenticated'
      return
    }
    
    loading.value = true
    message.value = ''
    error.value = ''
    
    const { error: updateError } = await supabase
      .from('profiles')
      .update({
        name: profile.value.name,
        phone: profile.value.phone,
        updated_at: new Date().toISOString()
      } as any)
      .eq('id', user.value.sub)
    
    if (updateError) {
      console.error('Error updating profile:', updateError)
      error.value = `Error updating profile: ${updateError.message}`
    } else {
      message.value = 'Profile updated successfully!'
      setTimeout(() => {
        message.value = ''
      }, 3000)
    }
    
    loading.value = false
  }
</script>