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
  source: z.string(), // 'crossover', 'urbandance', etc.
  classes: z.array(ExternalClassSchema),
  api_key: z.string(),
})

export default defineEventHandler(async (event) => {
  const supabase = useSupabaseClient(event)

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

  // Process each class
  for (const classData of classes) {
    try {
      // 1. Find or create choreographer
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
            is_independent: false
          })
          .select('id')
          .single()

        if (error) throw error
        choreographer = newChoreo
      }

      // 2. Find or create studio
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

      // 3. Upsert class
      const { error: upsertError } = await supabase
        .from('classes')
        .upsert({
          // Unique identifier for updates
          external_source: source,
          external_id: classData.external_id,

          // Class data
          booking_type: 'external',
          name: classData.name,
          choreographer_id: choreographer.id,
          studio_id: studio.id,
          external_booking_url: classData.external_booking_url,
          location: classData.location,
          start_time: classData.start_time,
          end_time: classData.end_time,
          level: classData.level,
          style: classData.style,
          last_synced_at: new Date().toISOString(),
          sync_status: 'active',
          status: 'published'
        }, {
          onConflict: 'external_source,external_id',
          ignoreDuplicates: false
        })

      if (upsertError) throw upsertError

      results.created++ // Note: can't easily distinguish created vs updated with upsert

    } catch (error: any) {
      results.errors.push({
        external_id: classData.external_id,
        error: error.message
      })
    }
  }

  // 4. Mark classes as deleted if not in this sync
  const externalIds = classes.map(c => c.external_id)
  const { error: deleteError } = await supabase
    .from('classes')
    .update({
      sync_status: 'deleted',
      status: 'cancelled'
    })
    .eq('external_source', source)
    .eq('booking_type', 'external')
    .not('external_id', 'in', `(${externalIds.join(',')})`)
    .eq('sync_status', 'active')

  if (deleteError) {
    console.error('Error marking deleted classes:', deleteError)
  }

  return {
    success: true,
    source,
    ...results
  }
})