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

  // Calculate date range: previous Monday to next Sunday (matching scraper logic)
  const today = new Date()
  // getDay() returns 0 (Sunday) to 6 (Saturday)
  // Convert to Monday=0, Sunday=6 format (like Python's weekday())
  const todayWeekday = today.getDay() === 0 ? 6 : today.getDay() - 1

  // Calculate previous Monday (Monday of current week)
  const previousMonday = new Date(today)
  previousMonday.setDate(today.getDate() - todayWeekday)
  previousMonday.setHours(0, 0, 0, 0)

  // Calculate next Sunday (Sunday of next week)
  // Formula: today + (14 - todayWeekday) days
  const daysToNextSunday = 14 - todayWeekday
  const nextSunday = new Date(today)
  nextSunday.setDate(today.getDate() + daysToNextSunday)
  nextSunday.setHours(23, 59, 59, 999)

  // Query classes with joins to choreographers and studios
  const { data: classes, error } = await supabase
    .from('classes')
    .select(`
      id,
      name,
      start_time,
      end_time,
      location,
      level,
      style,
      external_id,
      capacity,
      available_spots,
      external_booking_url,
      choreographers (
        id,
        name,
        instagram
      ),
      studios (
        id,
        name
      )
    `)
    .gte('start_time', previousMonday.toISOString())
    .lte('start_time', nextSunday.toISOString())
    .order('start_time', { ascending: true })

  if (error) {
    throw createError({
      statusCode: 500,
      message: `Error fetching classes: ${error.message}`
    })
  }

  // Transform database response to match Lesson type
  const lessons = (classes || []).map((classItem: any) => ({
    serviceId: classItem.external_id || '',
    start: classItem.start_time,
    end: classItem.end_time,
    name: classItem.name,
    location: classItem.location || '',
    totalSpots: classItem.total_spots ?? null,
    openSpots: classItem.open_spots ?? null,
    level: classItem.level || [],
    style: classItem.style || [],
    studio: classItem.studios?.name || '',
    choreo: {
      id: classItem.choreographers?.id || '',
      name: classItem.choreographers?.name || '',
      instagram: classItem.choreographers?.instagram || ''
    }
  }))

  return {
    lessons,
    dateRange: {
      start: previousMonday.toISOString(),
      end: nextSunday.toISOString()
    }
  }
})

