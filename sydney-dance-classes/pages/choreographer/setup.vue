<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="text-h5">
            Become a Choreographer
          </v-card-title>
          
          <v-card-text>
            <v-alert v-if="existingProfile" type="info" class="mb-4">
              You already have a choreographer profile. You can update it below.
            </v-alert>
            
            <v-form @submit.prevent="saveProfile">
              <v-text-field
                v-model="form.name"
                label="Stage/Display Name *"
                required
                hint="The name students will see"
              />
              
              <v-text-field
                v-model="form.instagram"
                label="Instagram Handle"
                placeholder="@yourhandle"
                prepend-icon="mdi-instagram"
              />
              
              <v-textarea
                v-model="form.bio"
                label="Bio"
                hint="Tell students about your dance background"
                rows="4"
              />
              
              <v-text-field
                v-model="form.email"
                label="Contact Email *"
                type="email"
                required
              />
              
              <v-text-field
                v-model="form.phone"
                label="Phone Number"
                type="tel"
              />
              
              <v-divider class="my-4" />
              
              <div class="text-subtitle-2 mb-2">As an independent choreographer:</div>
              <ul>
                <li>Create and manage your own classes</li>
                <li>Set your own prices and schedule</li>
                <li>Get paid directly (Stripe setup required later)</li>
                <li>Platform fee: $1 per booking</li>
              </ul>
              
              <v-alert v-if="error" type="error" class="mt-4">
                {{ error }}
              </v-alert>
              
              <v-alert v-if="success" type="success" class="mt-4">
                {{ success }}
              </v-alert>
              
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-4"
                :loading="loading"
                size="large"
              >
                {{ existingProfile ? 'Update Profile' : 'Create Choreographer Profile' }}
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
  middleware: 'auth' // Must be logged in
})

const supabase = useSupabaseClient()
const user = useSupabaseUser()
const router = useRouter()

const form = ref({
  name: '',
  instagram: '',
  bio: '',
  email: user.value?.email || '',
  phone: '',
})

const existingProfile = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref('')

// Load existing profile if it exists
onMounted(async () => {
  const { data } = await supabase
    .from('choreographers')
    .select('*')
    .eq('user_id', user.value.id)
    .single()
  
  if (data) {
    existingProfile.value = data
    form.value = {
      name: data.name,
      instagram: data.instagram || '',
      bio: data.bio || '',
      email: data.email || user.value.email,
      phone: data.phone || '',
    }
  }
})

const saveProfile = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    // Validate
    if (!form.value.name || !form.value.email) {
      throw new Error('Name and email are required')
    }
    
    const profileData = {
      user_id: user.value.id,
      name: form.value.name,
      instagram: form.value.instagram,
      bio: form.value.bio,
      email: form.value.email,
      phone: form.value.phone,
      updated_at: new Date().toISOString()
    }
    
    if (existingProfile.value) {
      // Update existing
      const { error: updateError } = await supabase
        .from('choreographers')
        .update(profileData)
        .eq('id', existingProfile.value.id)
      
      if (updateError) throw updateError
      
      success.value = 'Profile updated successfully!'
    } else {
      // Create new
      const { error: insertError } = await supabase
        .from('choreographers')
        .insert(profileData)
      
      if (insertError) throw insertError
      
      success.value = 'Choreographer profile created! Redirecting...'
      
      // Redirect to profile after 2 seconds
      setTimeout(() => {
        router.push('/profile')
      }, 2000)
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>