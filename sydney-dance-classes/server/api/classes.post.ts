import { z } from 'zod'
import { serverSupabaseClient, serverSupabaseServiceRole } from '#supabase/server'

// Validation schema for platform classes
const CreateClassSchema = z.object({
  name: z.string().min(1, 'Class name is required'),
  description: z.string().nullable().optional(),
  song: z.string().nullable().optional(), // NEW!
  location: z.string().min(1, 'Location is required'),
  start_time: z.string().datetime('Invalid start time format'),
  end_time: z.string().datetime('Invalid end time format'),
  timezone: z.string().default('Australia/Sydney'),
  level: z.array(z.string()).min(1, 'At least one difficulty level is required'),
  style: z.array(z.string()).min(1, 'At least one dance style is required'),
  price: z.number().positive('Price must be greater than 0'),
  capacity: z.number().int().positive('Capacity must be a positive integer'),
  available_spots: z.number().int().nonnegative('Available spots must be a non-negative integer'),
  status: z.enum(['draft', 'published'], {
    message: 'Status must be either draft or published'
  }).default('draft'),
}).refine(
  (data) => data.available_spots <= data.capacity,
  {
    message: 'Available spots cannot exceed capacity',
    path: ['available_spots']
  }
)

export default defineEventHandler(async (event) => {
  // 1. Authenticate
  const supabase = await serverSupabaseClient(event)
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    throw createError({
      statusCode: 401,
      message: 'Authentication required'
    })
  }

  // 2. Validate request body
  const body = await readBody(event)
  let validatedData
  try {
    validatedData = CreateClassSchema.parse(body)
  } catch (error: any) {
    throw createError({
      statusCode: 400,
      message: error.errors?.[0]?.message || 'Invalid request data'
    })
  }

  const {
    name,
    start_time,
    end_time,
    location,
    timezone,
    level,
    style,
    description,
    song, // NEW!
    price,
    capacity,
    available_spots,
    status
  } = validatedData

  // 3. Get or create choreographer
  const supabaseAdmin = await serverSupabaseServiceRole(event)

  let { data: choreographer } = await supabaseAdmin
    .from('choreographers')
    .select('id')
    .eq('user_id', user.id)
    .maybeSingle()

  let choreographerId: string

  if (!choreographer) {
    const { data: newChoreo, error: choreoError } = await supabaseAdmin
      .from('choreographers')
      .insert({
        user_id: user.id,
        name: user.email?.split('@')[0] || 'Unknown Choreographer'
      })
      .select('id')
      .single()

    if (choreoError || !newChoreo) {
      console.error('Failed to create choreographer:', choreoError)
      throw createError({
        statusCode: 500,
        message: `Failed to create choreographer profile: ${choreoError?.message || 'Unknown error'}`
      })
    }
    choreographerId = newChoreo.id
  } else {
    choreographerId = choreographer.id
  }

  // 4. Verify ownership
  const { data: ownerCheck } = await supabaseAdmin
    .from('choreographers')
    .select('user_id')
    .eq('id', choreographerId)
    .single()

  if (ownerCheck?.user_id !== user.id) {
    throw createError({
      statusCode: 403,
      message: 'Unauthorized to create classes for this choreographer'
    })
  }

  // 5. Insert class
  const { data: newClass, error: insertError } = await supabaseAdmin
    .from('classes')
    .insert({
      name,
      description: description || null,
      song: song || null, // NEW!
      choreographer_id: choreographerId,
      booking_type: 'platform',
      external_source: 'user_created',
      external_id: null,
      external_booking_url: null,
      studio_id: null,
      location,
      level,
      style,
      status,
      price,
      capacity,
      available_spots,
      start_time,
      end_time,
      timezone,
      last_synced_at: new Date().toISOString()
    })
    .select()
    .single()

  if (insertError) {
    console.error('Failed to insert class:', insertError)
    throw createError({
      statusCode: 500,
      message: `Failed to create class: ${insertError.message}`
    })
  }

  return {
    success: true,
    class: newClass
  }
})