import { createClient } from '@supabase/supabase-js'

export default defineEventHandler(async (event) => {
  // Create Supabase client with service role (bypasses RLS)
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false
      }
    }
  )

  // Get API key from query parameter
  const query = getQuery(event)
  const api_key = query.api_key as string

  // Verify API key
  if (!api_key || api_key !== process.env.SYNC_API_KEY) {
    throw createError({
      statusCode: 401,
      message: 'Invalid API key'
    })
  }

  // Delete all existing external classes
  const { data, error: deleteError } = await supabase
    .from('classes')
    .delete()
    .eq('booking_type', 'external')
    .select()

  if (deleteError) {
    throw createError({
      statusCode: 500,
      message: `Failed to delete external classes: ${deleteError.message}`
    })
  }

  const deletedCount = data?.length || 0

  return {
    success: true,
    deleted: deletedCount
  }
})

