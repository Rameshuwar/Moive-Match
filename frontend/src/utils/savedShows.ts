import type { ShowResult } from '../api/movieMatchApi'

const STORAGE_KEY = 'moviematch_saved_shows'

export interface SavedShow extends ShowResult {
  id: string
}

function createShowId(show: ShowResult): string {
  return [
    show.movie,
    show.theatre,
    show.show_time,
    show.language,
  ]
    .join('|')
    .toLowerCase()
}

export function getSavedShows(): SavedShow[] {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)

    if (!stored) {
      return []
    }

    return JSON.parse(stored) as SavedShow[]
  } catch (error) {
    console.error('Unable to read saved shows:', error)
    return []
  }
}

export function isShowSaved(show: ShowResult): boolean {
  const savedShows = getSavedShows()

  const id = createShowId(show)

  return savedShows.some((savedShow) => savedShow.id === id)
}

export function saveShow(show: ShowResult): SavedShow[] {
  const savedShows = getSavedShows()

  const id = createShowId(show)

  if (savedShows.some((savedShow) => savedShow.id === id)) {
    return savedShows
  }

  const savedShow: SavedShow = {
    ...show,
    id,
  }

  const updatedShows = [...savedShows, savedShow]

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(updatedShows),
  )

  return updatedShows
}

export function removeSavedShow(show: ShowResult): SavedShow[] {
  const savedShows = getSavedShows()

  const id = createShowId(show)

  const updatedShows = savedShows.filter(
    (savedShow) => savedShow.id !== id,
  )

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(updatedShows),
  )

  return updatedShows
}

export function toggleSavedShow(show: ShowResult): SavedShow[] {
  if (isShowSaved(show)) {
    return removeSavedShow(show)
  }

  return saveShow(show)
}
