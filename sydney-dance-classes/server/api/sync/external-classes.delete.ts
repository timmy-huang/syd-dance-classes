import { createClient } from '@supabase/supabase-js'
import { z } from 'zod'

const DeleteRequestSchema = z.object({
  api_key: z.string(),
})

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

  // Parse request
  const body = await readBody(event)
  const { api_key } = DeleteRequestSchema.parse(body)

  // Verify API key
  if (api_key !== process.env.SYNC_API_KEY) {
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

