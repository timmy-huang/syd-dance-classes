import { z } from 'zod'
import { serverSupabaseServiceRole } from '#supabase/server'

// Validation schema
const QuestionAnswerSchema = z.object({
  question_number: z.number().int().positive('Question number must be positive'),
  video_id: z.string().min(1, 'Video ID is required'),
  guess: z.string().min(1, 'Guess is required'),
  correct: z.boolean()
})

export default defineEventHandler(async (event) => {
  // Parse and validate request body
  const body = await readBody(event)

  let validatedData
  try {
    validatedData = QuestionAnswerSchema.parse(body)
  } catch (error: any) {
    throw createError({
      statusCode: 400,
      message: error.errors?.[0]?.message || 'Invalid request data'
    })
  }

  const { question_number, video_id, guess, correct } = validatedData

  // Use service role since we're allowing public inserts
  const supabase = await serverSupabaseServiceRole(event)

  // Insert into database
  const { data, error: insertError } = await supabase
    .from('cg_question_answers')
    .insert({
      question_number,
      video_id,
      guess,
      correct
    })
    .select()
    .single()

  if (insertError) {
    console.error('Failed to insert question answer:', insertError)
    throw createError({
      statusCode: 500,
      message: `Failed to save question answer: ${insertError.message}`
    })
  }

  return {
    success: true,
    data
  }
})