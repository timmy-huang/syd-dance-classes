<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card>
          <v-card-title class="text-h5 mb-4">Create a Class</v-card-title>
          
          <v-card-text>
            <v-form ref="form" @submit.prevent="submitClass">
              <!-- Class Name -->
              <v-text-field
                v-model="formData.name"
                label="Class Name"
                :rules="[rules.required]"
                required
                class="mb-3"
              />

              <!-- Description -->
              <v-textarea
                v-model="formData.description"
                label="Description (Optional)"
                rows="4"
                class="mb-3"
              />

              <!-- Location/Venue -->
              <v-text-field
                v-model="formData.location"
                label="Location / Venue"
                :rules="[rules.required]"
                required
                class="mb-3"
              />

              <!-- Date and Time -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.date"
                    label="Date"
                    type="date"
                    :rules="[rules.required]"
                    required
                    class="mb-3"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="formData.startTime"
                    label="Start Time"
                    type="time"
                    :rules="[rules.required]"
                    required
                    class="mb-3"
                  />
                </v-col>
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="formData.endTime"
                    label="End Time"
                    type="time"
                    :rules="[rules.required]"
                    required
                    class="mb-3"
                  />
                </v-col>
              </v-row>

              <!-- Timezone -->
              <v-select
                v-model="formData.timezone"
                label="Timezone"
                :items="timezones"
                :rules="[rules.required]"
                required
                class="mb-3"
              />

              <!-- Level (Multi-select) -->
              <v-select
                v-model="formData.level"
                label="Difficulty Level"
                :items="levelOptions"
                multiple
                :rules="[rules.requiredArray]"
                required
                class="mb-3"
                hint="Select one or more difficulty levels"
                persistent-hint
              />

              <!-- Style (Multi-select) -->
              <v-select
                v-model="formData.style"
                label="Dance Style"
                :items="styleOptions"
                multiple
                :rules="[rules.requiredArray]"
                required
                class="mb-3"
                hint="Select one or more dance styles"
                persistent-hint
              />

              <!-- Price -->
              <v-text-field
                v-model.number="formData.price"
                label="Price (AUD)"
                type="number"
                step="0.01"
                min="0"
                :rules="[rules.required, rules.positiveNumber]"
                required
                prepend-inner-icon="mdi-currency-usd"
                class="mb-3"
              />

              <!-- Capacity -->
              <v-text-field
                v-model.number="formData.capacity"
                label="Total Capacity"
                type="number"
                min="1"
                :rules="[rules.required, rules.positiveInteger]"
                required
                class="mb-3"
              />

              <!-- Available Spots -->
              <v-text-field
                v-model.number="formData.available_spots"
                label="Available Spots"
                type="number"
                min="0"
                :rules="[rules.required, rules.nonNegativeInteger, rules.availableSpotsValid]"
                required
                class="mb-3"
                hint="Must be less than or equal to capacity"
                persistent-hint
              />

              <!-- Status -->
              <v-select
                v-model="formData.status"
                label="Status"
                :items="statusOptions"
                :rules="[rules.required]"
                required
                class="mb-3"
                hint="Draft classes are not visible to the public"
                persistent-hint
              />

              <!-- Success/Error Messages -->
              <v-alert
                v-if="message"
                :type="messageType"
                class="mt-4"
                closable
                @click:close="message = ''"
              >
                {{ message }}
              </v-alert>

              <!-- Submit Button -->
              <div class="d-flex justify-end mt-4">
                <v-btn
                  type="submit"
                  color="primary"
                  :loading="loading"
                  :disabled="loading"
                >
                  Create Class
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { styles } from '~/utils/consts'

  interface Profile {
    id: string
    email: string | null
    name: string | null
    phone: string | null
    created_at?: string
    updated_at?: string
  }

  definePageMeta({
    middleware: 'auth' // Only logged-in users can access
  })

  const supabase = useSupabaseClient()
  const user = useSupabaseUser()
  const router = useRouter()

  const form = ref<any>(null)
  const loading = ref(false)
  const message = ref('')
  const messageType = ref<'success' | 'error' | 'info' | 'warning'>('success')

  const levelOptions = [
    'beginner',
    'intermediate',
    'advanced',
    'pop-up',
    'youth'
  ]

  const styleOptions = styles

  const timezones = [
    { title: 'Australia/Sydney (AEST/AEDT)', value: 'Australia/Sydney' },
    { title: 'Australia/Melbourne (AEST/AEDT)', value: 'Australia/Melbourne' },
    { title: 'Australia/Brisbane (AEST)', value: 'Australia/Brisbane' },
    { title: 'Australia/Adelaide (ACST/ACDT)', value: 'Australia/Adelaide' },
    { title: 'Australia/Perth (AWST)', value: 'Australia/Perth' }
  ]

  const statusOptions = [
    { title: 'Draft', value: 'draft' },
    { title: 'Published', value: 'published' }
  ]

  const formData = ref({
    name: '',
    description: '',
    location: '',
    date: '',
    startTime: '',
    endTime: '',
    timezone: 'Australia/Sydney',
    level: [] as string[],
    style: [] as string[],
    price: null as number | null,
    capacity: null as number | null,
    available_spots: null as number | null,
    status: 'draft' as 'draft' | 'published'
  })

  const rules = {
    required: (value: any) => !!value || 'This field is required',
    requiredArray: (value: any[]) => (value && value.length > 0) || 'Please select at least one option',
    positiveNumber: (value: number) => value > 0 || 'Price must be greater than 0',
    positiveInteger: (value: number) => (Number.isInteger(value) && value > 0) || 'Capacity must be a positive integer',
    nonNegativeInteger: (value: number) => (Number.isInteger(value) && value >= 0) || 'Available spots must be a non-negative integer',
    availableSpotsValid: (value: number) => {
      if (formData.value.capacity === null) return true
      return value <= formData.value.capacity || 'Available spots cannot exceed capacity'
    }
  }

  const submitClass = async () => {
  if (!form.value) return
  const { valid } = await form.value.validate()
  if (!valid) {
    message.value = 'Please fill in all required fields'
    messageType.value = 'error'
    return
  }

  loading.value = true
  message.value = ''

  try {
    const startDateTime = new Date(`${formData.value.date}T${formData.value.startTime}`)
    const endDateTime = new Date(`${formData.value.date}T${formData.value.endTime}`)

    if (endDateTime <= startDateTime) {
      throw new Error('End time must be after start time')
    }

    if (formData.value.available_spots! > formData.value.capacity!) {
      throw new Error('Available spots cannot exceed capacity')
    }

    const classPayload = {
      name: formData.value.name,
      description: formData.value.description || null,
      location: formData.value.location,
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString(),
      timezone: formData.value.timezone,
      level: formData.value.level,
      style: formData.value.style,
      price: formData.value.price!,
      capacity: formData.value.capacity!,
      available_spots: formData.value.available_spots!,
      status: formData.value.status
    }

    // ✅ Simple call - auth handled automatically via cookies
    const response = await $fetch('/api/classes', {
      method: 'POST',
      body: classPayload
    })

    if (response.success) {
      message.value = formData.value.status === 'published' 
        ? 'Class created and published successfully!'
        : 'Class created as draft successfully!'
      messageType.value = 'success'

      // Reset form
      formData.value = {
        name: '',
        description: '',
        location: '',
        date: '',
        startTime: '',
        endTime: '',
        timezone: 'Australia/Sydney',
        level: [],
        style: [],
        price: null,
        capacity: null,
        available_spots: null,
        status: 'draft'
      }
      form.value?.reset()

      setTimeout(() => {
        router.push('/classes')
      }, 2000)
    }
  } catch (error: any) {
    console.error('Error creating class:', error)
    message.value = error.data?.message || error.message || 'Error creating class. Please try again.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

