<template>
  <ClientOnly>
    <!-- Show if user is logged in -->
    <div v-if="user">
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind='props'>
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        
        <v-list>
          <v-list-item>
            <v-list-item-title>{{ user.email }}</v-list-item-title>
          </v-list-item>
          
          <v-divider />
          
          <v-list-item @click='goToProfile'>
            <template v-slot:prepend>
              <v-icon>mdi-account</v-icon>
            </template>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          
          <v-list-item @click='handleLogout'>
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
    
    <!-- Show if user is NOT logged in -->
    <v-btn v-else @click='goToLogin' variant='text'>
      Login
    </v-btn>
  </ClientOnly>
</template>

<script setup>
const supabase = useSupabaseClient()
const user = useSupabaseUser()
const router = useRouter()

const goToLogin = () => router.push('/login')
const goToProfile = () => router.push('/profile')

const handleLogout = async () => {
  await supabase.auth.signOut()
  router.push('/')
}
</script>
