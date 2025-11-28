<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <!-- Show redirect message if present -->
        <v-alert
          v-if="redirectMessage"
          type="info"
          variant="tonal"
          class="mb-4"
          closable
        >
          {{ redirectMessage }}
        </v-alert>
        <v-card>
          <v-card-title>My Profile</v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
              <!-- Profile Photo Upload -->
              <div class="mb-6">
                <v-label class="mb-2">Profile Photo</v-label>
                <div class="d-flex align-center gap-4">
                  <v-avatar size="100" color="grey-lighten-2">
                    <v-img
                      v-if="profilePhotoUrl"
                      :src="profilePhotoUrl"
                      cover
                    />
                    <v-icon v-else size="50" icon="mdi-account-circle" />
                  </v-avatar>
                  
                  <div>
                    <v-file-input
                      ref="fileInput"
                      v-model="photoFile"
                      accept="image/*"
                      label="Choose photo"
                      prepend-icon="mdi-camera"
                      variant="outlined"
                      density="compact"
                      :loading="uploadingPhoto"
                      @change="handlePhotoUpload"
                    />
                    <v-btn
                      v-if="profilePhotoUrl"
                      variant="text"
                      color="error"
                      size="small"
                      @click="removePhoto"
                    >
                      Remove Photo
                    </v-btn>
                  </div>
                </div>
              </div>

              <!-- Email (readonly) -->
              <v-text-field
                v-model="profile.email"
                label="Email"
                disabled
                class="mb-3"
              />
              
              <!-- Name -->
              <v-text-field
                v-model="profile.name"
                label="Name *"
                :rules="[rules.required]"
                required
                class="mb-3"
              />

              <!-- Description/Bio -->
              <v-textarea
                v-model="profile.description"
                label="Bio / Description"
                rows="4"
                hint="Tell us about yourself and your dance background"
                persistent-hint
                counter="500"
                :rules="[rules.maxLength(500)]"
                class="mb-3"
              />

              <!-- Instagram Handle -->
              <v-text-field
                v-model="profile.instagram_handle"
                label="Instagram Handle"
                prepend-inner-icon="mdi-instagram"
                placeholder="@yourusername"
                hint="Enter your Instagram handle (with or without @)"
                persistent-hint
                :rules="[rules.instagram]"
                class="mb-3"
              />
              
              <!-- Phone -->
              <v-text-field
                v-model="profile.phone"
                label="Phone"
                prepend-inner-icon="mdi-phone"
                class="mb-3"
              />

              <!-- Profile Completion Status -->
              <v-alert
                v-if="!isProfileComplete"
                type="warning"
                variant="tonal"
                class="mt-4"
              >
                <v-alert-title>Profile Incomplete</v-alert-title>
                Complete your profile to create classes. Required fields: Profile Photo, Name, Description, Instagram Handle, Phone
              </v-alert>

              <v-alert
                v-else
                type="success"
                variant="tonal"
                class="mt-4"
              >
                <v-alert-title>Profile Complete!</v-alert-title>
                You can now create classes.
              </v-alert>
              
              <!-- Error/Success Messages -->
              <v-alert v-if="error" type="error" class="mt-4">
                {{ error }}
              </v-alert>
              
              <v-alert v-if="message" type="success" class="mt-4">
                {{ message }}
              </v-alert>
              
              <!-- Submit Button -->
              <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                class="mt-4"
                block
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

  const route = useRoute()
  const redirectMessage = computed(() => route.query.message as string)

  interface Profile {
    id: string
    email: string | null
    name: string | null
    phone: string | null
    profile_photo_url: string | null
    description: string | null
    instagram_handle: string | null
    created_at?: string
    updated_at?: string
  }

  const supabase = useSupabaseClient()
  const user = useSupabaseUser()

  const profile = ref({
    email: '',
    name: '',
    phone: '',
    description: '',
    instagram_handle: ''
  })

  const profilePhotoUrl = ref<string | null>(null)
  const photoFile = ref<File[]>([])
  const fileInput = ref<any>(null)

  const loading = ref(false)
  const uploadingPhoto = ref(false)
  const message = ref('')
  const error = ref('')

  const rules = {
    required: (value: any) => !!value || 'This field is required',
    maxLength: (max: number) => (value: string) => 
      !value || value.length <= max || `Maximum ${max} characters`,
    instagram: (value: string) => {
      if (!value) return true
      // Remove @ if present
      const handle = value.replace('@', '')
      // Instagram username rules: 1-30 chars, alphanumeric, dots, underscores
      const regex = /^[a-zA-Z0-9._]{1,30}$/
      return regex.test(handle) || 'Invalid Instagram handle'
    }
  }

  const isProfileComplete = computed(() => {
    // Required fields for creating classes
    return !!(profile.value.name && profile.value.description && profile.value.instagram_handle && profile.value.phone && profile.value.profile_photo_url)
  })

  const loadProfile = async () => {
    console.log('loadProfile')
    if (!user.value?.sub) {
      error.value = 'No user ID found'
      return
    }
    
    loading.value = true
    
    try {
      const { data, error: fetchError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.value.sub)
        .single()
      
      if (fetchError) {
        console.error('Error loading profile:', fetchError)
        error.value = `Error loading profile: ${fetchError.message}`
        return
      }
      
      if (data) {
        console.log('data', data)
        const profileData = data as Profile
        
        profile.value = {
          email: profileData.email || user.value.email || '',
          name: profileData.name || '',
          phone: profileData.phone || '',
          description: profileData.description || '',
          instagram_handle: profileData.instagram_handle || ''
        }
        
        profilePhotoUrl.value = profileData.profile_photo_url
      }
    } catch (err: any) {
      console.error('Unexpected error:', err)
      error.value = 'Unexpected error loading profile'
    } finally {
      loading.value = false
    }
  }

  // Watch for user to become available
  watch(user, async (newUser) => {
    console.log('user', newUser)
    if (newUser?.sub) {
      await loadProfile()
    }
  }, { immediate: true })

  const handlePhotoUpload = async () => {
    if (!photoFile.value || photoFile.value.length === 0) return
    
    const file = photoFile.value[0]
    
    // Validate file
    if (!file.type.startsWith('image/')) {
      error.value = 'Please upload an image file'
      photoFile.value = []
      return
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      error.value = 'Image must be less than 5MB'
      photoFile.value = []
      return
    }
    
    uploadingPhoto.value = true
    error.value = ''
    
    try {
      // Delete old photo if exists
      if (profilePhotoUrl.value) {
        const oldPath = profilePhotoUrl.value.split('/').pop()
        if (oldPath) {
          await supabase.storage
            .from('profile-photos')
            .remove([`${user.value!.sub}/${oldPath}`])
        }
      }
      
      // Upload new photo
      const fileExt = file.name.split('.').pop()
      const fileName = `${Date.now()}.${fileExt}`
      const filePath = `${user.value!.sub}/${fileName}`
      
      const { error: uploadError } = await supabase.storage
        .from('profile-photos')
        .upload(filePath, file)
      
      if (uploadError) {
        throw uploadError
      }
      
      // Get public URL
      const { data: urlData } = supabase.storage
        .from('profile-photos')
        .getPublicUrl(filePath)
      
      profilePhotoUrl.value = urlData.publicUrl
      
      // Update profile in database
      const { error: updateError } = await supabase
        .from('profiles')
        .update({
          profile_photo_url: profilePhotoUrl.value,
          updated_at: new Date().toISOString()
        })
        .eq('id', user.value!.sub)
      
      if (updateError) {
        throw updateError
      }
      
      message.value = 'Profile photo updated successfully!'
      setTimeout(() => {
        message.value = ''
      }, 3000)
    } catch (err: any) {
      console.error('Error uploading photo:', err)
      error.value = `Failed to upload photo: ${err.message}`
    } finally {
      uploadingPhoto.value = false
      photoFile.value = []
    }
  }

  const removePhoto = async () => {
    if (!profilePhotoUrl.value) return
    
    uploadingPhoto.value = true
    error.value = ''
    
    try {
      // Delete from storage
      const path = profilePhotoUrl.value.split('/').pop()
      if (path) {
        await supabase.storage
          .from('profile-photos')
          .remove([`${user.value!.sub}/${path}`])
      }
      
      // Update profile in database
      const { error: updateError } = await supabase
        .from('profiles')
        .update({
          profile_photo_url: null,
          updated_at: new Date().toISOString()
        })
        .eq('id', user.value!.sub)
      
      if (updateError) {
        throw updateError
      }
      
      profilePhotoUrl.value = null
      message.value = 'Profile photo removed successfully!'
      setTimeout(() => {
        message.value = ''
      }, 3000)
    } catch (err: any) {
      console.error('Error removing photo:', err)
      error.value = `Failed to remove photo: ${err.message}`
    } finally {
      uploadingPhoto.value = false
    }
  }

  const updateProfile = async () => {
    if (!user.value?.sub) {
      error.value = 'User not authenticated'
      return
    }
    
    loading.value = true
    message.value = ''
    error.value = ''
    
    try {
      // Normalize Instagram handle (remove @ if present)
      let instagramHandle = profile.value.instagram_handle.trim()
      if (instagramHandle && instagramHandle.startsWith('@')) {
        instagramHandle = instagramHandle.substring(1)
      }
      
      const { error: updateError } = await supabase
        .from('profiles')
        .update({
          name: profile.value.name,
          phone: profile.value.phone,
          description: profile.value.description,
          instagram_handle: instagramHandle || null,
          updated_at: new Date().toISOString()
        })
        .eq('id', user.value.sub)
      
      if (updateError) {
        throw updateError
      }
      
      message.value = 'Profile updated successfully!'
      setTimeout(() => {
        message.value = ''
      }, 3000)
    } catch (err: any) {
      console.error('Error updating profile:', err)
      error.value = `Error updating profile: ${err.message}`
    } finally {
      loading.value = false
    }
  }
</script>

<style scoped>
.gap-4 {
  gap: 1rem;
}
</style>