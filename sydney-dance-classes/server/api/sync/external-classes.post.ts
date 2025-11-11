import { createClient } from '@supabase/supabase-js'
import { z } from 'zod'

// Validation schema
const ExternalClassSchema = z.object({
  external_id: z.string(),
  name: z.string(),
  choreographer_name: z.string(),
  choreographer_instagram: z.string().optional(),
  studio_name: z.string(),
  external_booking_url: z.string().url(),
  start_time: z.string(), // ISO datetime
  end_time: z.string(),
  location: z.string(),
  level: z.array(z.string()),
  style: z.array(z.string()),
})

const SyncRequestSchema = z.object({
  source: z.string(),
  classes: z.array(ExternalClassSchema),
  api_key: z.string(),
})

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

  // Parse request
  const body = await readBody(event)
  const { source, classes, api_key } = SyncRequestSchema.parse(body)

  // Verify API key
  if (api_key !== process.env.SYNC_API_KEY) {
    throw createError({
      statusCode: 401,
      message: 'Invalid API key'
    })
  }

  const results = {
    created: 0,
    updated: 0,
    errors: [] as any[]
  }

  // 2. Process and insert each class
  for (const classData of classes) {
    try {
      // Find or create choreographer
      let { data: choreographer } = await supabase
        .from('choreographers')
        .select('id')
        .eq('name', classData.choreographer_name)
        .maybeSingle()

      if (!choreographer) {
        const { data: newChoreo, error } = await supabase
          .from('choreographers')
          .insert({
            name: classData.choreographer_name,
            instagram: classData.choreographer_instagram,
          })
          .select('id')
          .single()

        if (error) throw error
        choreographer = newChoreo
      }

      // Find or create studio
      let { data: studio } = await supabase
        .from('studios')
        .select('id')
        .eq('name', classData.studio_name)
        .maybeSingle()

      if (!studio) {
        const { data: newStudio, error } = await supabase
          .from('studios')
          .insert({
            name: classData.studio_name,
            external_booking_url: classData.external_booking_url
          })
          .select('id')
          .single()

        if (error) throw error
        studio = newStudio
      }

      // Insert new class
      const classPayload = {
        booking_type: 'external' as const,
        name: classData.name,
        choreographer_id: choreographer.id,
        studio_id: studio.id,
        external_source: source,
        external_id: classData.external_id,
        external_booking_url: classData.external_booking_url,
        location: classData.location,
        start_time: classData.start_time,
        end_time: classData.end_time,
        level: classData.level,
        style: classData.style,
        last_synced_at: new Date().toISOString(),
        sync_status: 'active',
        status: 'published'
      }

      const { error: insertError } = await supabase
        .from('classes')
        .insert(classPayload)

      if (insertError) throw insertError
      results.created++

    } catch (error: any) {
      results.errors.push({
        external_id: classData.external_id,
        error: error.message
      })
    }
  }

  return {
    success: true,
    source,
    ...results
  }
})