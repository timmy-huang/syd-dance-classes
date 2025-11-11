export const useStudios = () => {
  const studios = useState<string[]>('studios', () => [])

  const fetchStudios = async () => {
    // If already loaded, return cached value
    if (studios.value.length > 0) {
      return studios.value
    }

    try {
      const response = await $fetch<{ studios: string[] }>('/api/studios')
      studios.value = response.studios
      return studios.value
    } catch (error) {
      console.error('Error fetching studios:', error)
      // Return empty array on error to prevent crashes
      return []
    }
  }

  return {
    studios: readonly(studios),
    fetchStudios
  }
}

