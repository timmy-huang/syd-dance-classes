import { createClient } from '@supabase/supabase-js'

export default defineEventHandler(async (event) => {
  // Create Supabase client with service role (bypasses RLS)
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SECRET_KEY!,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false
      }
    }
  )

  // Query all studios, ordered by name
  const { data: studios, error } = await supabase
    .from('studios')
    .select('id, name')
    .order('name', { ascending: true })

  if (error) {
    throw createError({
      statusCode: 500,
      message: `Error fetching studios: ${error.message}`
    })
  }

  // Return just the studio names as an array (matching the current format)
  return {
    studios: (studios || []).map((studio: any) => studio.name)
  }
})

