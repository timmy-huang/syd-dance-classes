import { z } from 'zod'
import { serverSupabaseServiceRole } from '#supabase/server'

// Validation schema
const DifficultySchema = z.object({
  difficulty: z.string().min(1, 'Difficulty is required')
})

export default defineEventHandler(async (event) => {
  // Parse and validate request body
  const body = await readBody(event)

  let validatedData
  try {
    validatedData = DifficultySchema.parse(body)
  } catch (error: any) {
    throw createError({
      statusCode: 400,
      message: error.errors?.[0]?.message || 'Invalid request data'
    })
  }

  const { difficulty } = validatedData

  // Use service role since we're allowing public inserts
  const supabase = await serverSupabaseServiceRole(event)

  // Insert into database
  const { data, error: insertError } = await supabase
    .from('cg_difficulty')
    .insert({
      difficulty
    })
    .select()
    .single()

  if (insertError) {
    console.error('Failed to insert difficulty:', insertError)
    throw createError({
      statusCode: 500,
      message: `Failed to save difficulty: ${insertError.message}`
    })
  }

  return {
    success: true,
    data
  }
})