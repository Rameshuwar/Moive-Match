const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface SearchRequest {
  location: string
  date: string
  start_time: string
  end_time: string
  max_price: number
}

export interface ShowResult {
  movie: string
  poster_url: string | null
  language: string
  duration_minutes: number
  theatre: string
  show_time: string
  ticket_price: number
  available_seats: number
}

export interface SearchResponse {
  message: string
  total_results: number
  results: ShowResult[]
}

export async function searchShows(
  request: SearchRequest,
): Promise<SearchResponse> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    throw new Error(`Search failed with status ${response.status}`)
  }

  return response.json()
}
