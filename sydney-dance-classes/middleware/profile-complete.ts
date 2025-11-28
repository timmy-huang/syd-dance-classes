export default defineNuxtRouteMiddleware(async (to, from) => {
  const supabase = useSupabaseClient()
  const user = useSupabaseUser()

  if (!user.value) {
    return navigateTo('/login')
  }

  // Check if profile is complete
  const { data: profile } = await supabase
    .from('profiles')
    .select('name')
    .eq('id', user.value.id)
    .single()

  // TODO check profile completions (name, description, instagram_handle, phone)

  if (!profile?.name) {
    // Profile incomplete, redirect to profile page
    return navigateTo({
      path: '/profile',
      query: {
        redirect: to.fullPath,
        message: 'Please complete your profile before creating classes'
      }
    })
  }
})