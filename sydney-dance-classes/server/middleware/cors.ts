export default defineEventHandler((event) => {
  // Only handle /api/cg routes
  if (event.path?.startsWith('/api/cg')) {
    // Set CORS headers
    setResponseHeaders(event, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    })

    // Handle OPTIONS preflight
    if (event.method === 'OPTIONS') {
      setResponseStatus(event, 204)
      return '' // Stop processing here
    }
  }
})