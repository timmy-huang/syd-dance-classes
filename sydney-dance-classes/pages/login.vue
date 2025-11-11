<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-h5 text-center">
            {{ isSignUp ? 'Sign Up' : 'Login' }}
          </v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleAuth">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                required
                prepend-icon="mdi-email"
              />
              
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                prepend-icon="mdi-lock"
              />
              
              <v-text-field
                v-if="isSignUp"
                v-model="name"
                label="Name"
                prepend-icon="mdi-account"
              />
              
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
              >
                {{ isSignUp ? 'Sign Up' : 'Login' }}
              </v-btn>
            </v-form>
            
            <v-divider class="my-4" />
            
            <v-btn
              @click="isSignUp = !isSignUp"
              variant="text"
              block
            >
              {{ isSignUp ? 'Already have an account? Login' : "Don't have an account? Sign up" }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const supabase = useSupabaseClient()
const router = useRouter()

const email = ref('')
const password = ref('')
const name = ref('')
const isSignUp = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleAuth = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    if (isSignUp.value) {
      // Sign up
      const { data, error: signUpError } = await supabase.auth.signUp({
        email: email.value,
        password: password.value,
        options: {
          data: {
            name: name.value
          }
        }
      })
      
      if (signUpError) throw signUpError
      
      success.value = 'Check your email to confirm your account!'
    } else {
      // Login
      const { data, error: loginError } = await supabase.auth.signInWithPassword({
        email: email.value,
        password: password.value
      })
      
      if (loginError) throw loginError
      
      // Redirect to home
      router.push('/')
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>