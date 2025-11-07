import type { Lesson } from '~/types'

const getData = async (lessons: Ref<Lesson[]>) => {
  try {
    // Fetch all classes from the database API
    const response = await fetch('/api/classes')

    if (!response.ok) {
      throw new Error(`Failed to fetch classes: ${response.statusText}`)
    }

    const result = await response.json()
    const data = result.lessons || []

    // Transform API response to match Lesson type
    data.forEach((lesson: any) => {
      lessons.value.push({
        serviceId: lesson.serviceId,
        start: new Date(lesson.start),
        end: new Date(lesson.end),
        name: lesson.name,
        location: lesson.location,
        totalSpots: lesson.totalSpots,
        openSpots: lesson.openSpots,
        level: lesson.level || [],
        style: lesson.style || [],
        studio: lesson.studio,
        choreo: {
          id: lesson.choreo.id || '',
          name: lesson.choreo.name || '',
          instagram: lesson.choreo.instagram || ''
        }
      })
    })

    console.log('All data fetched from database, lessons count:', lessons.value.length)
    return lessons
  } catch (error) {
    console.error('Error fetching data from database:', error)
    return lessons
  }
}

export default getData