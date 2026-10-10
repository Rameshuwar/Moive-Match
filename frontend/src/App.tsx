import { useState } from 'react'
import ShowCard from './components/ShowCard'
import { searchShows } from './api/movieMatchApi'
import {
  getSavedShows,
  isShowSaved,
  toggleSavedShow,
} from './utils/savedShows'

type MatchingShow = {
  original: {
    movie: string
    poster_url: string | null
    language: string
    duration_minutes: number
    theatre: string
    show_time: string
    ticket_price: number
    available_seats: number
  }

  movieTitle: string
  poster: string
  language: string
  format: string
  duration: string
  theatre: string
  showTime: string
  price: number
  availableSeats: number
}

function App() {
  const [location, setLocation] = useState('Salem')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [maxPrice, setMaxPrice] = useState('')

  const [matchingShows, setMatchingShows] = useState<
    MatchingShow[]
  >([])

  const [savedShows, setSavedShows] = useState(
    getSavedShows(),
  )

  const [isSearching, setIsSearching] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const [searchError, setSearchError] = useState('')
  const [lastUpdated, setLastUpdated] = useState('just now')

  /*
   * The backend expects:
   *
   * start_time
   * end_time
   *
   * We convert the UI time options into backend time ranges.
   */
  const timeRanges: Record<
    string,
    {
      start_time: string
      end_time: string
    }
  > = {
    Morning: {
      start_time: '06:00',
      end_time: '12:00',
    },
    Afternoon: {
      start_time: '12:00',
      end_time: '17:00',
    },
    Evening: {
      start_time: '17:00',
      end_time: '21:00',
    },
    Night: {
      start_time: '21:00',
      end_time: '23:59',
    },
  }

  /*
   * Convert backend search results into the structure
   * expected by ShowCard.
   *
   * We keep the original backend result inside `original`
   * so saved shows can use the exact backend data without
   * converting display values back into backend values.
   */
  const convertResultsToShows = (
    results: {
      movie: string
      poster_url: string | null
      language: string
      duration_minutes: number
      theatre: string
      show_time: string
      ticket_price: number
      available_seats: number
    }[],
  ): MatchingShow[] => {
    return results.map((show) => ({
      original: show,

      movieTitle: show.movie,
      poster: show.poster_url ?? '',
      language: show.language,
      format: '2D',
      duration: formatDuration(show.duration_minutes),
      theatre: show.theatre,
      showTime: formatShowTime(show.show_time),
      price: show.ticket_price,
      availableSeats: show.available_seats,
    }))
  }

  /*
   * Convert movie duration in minutes into a readable format.
   *
   * Examples:
   * 169 -> 2h 49m
   * 120 -> 2h
   * 45  -> 45m
   */
  const formatDuration = (minutes: number): string => {
    const hours = Math.floor(minutes / 60)
    const remainingMinutes = minutes % 60

    if (hours === 0) {
      return `${remainingMinutes}m`
    }

    if (remainingMinutes === 0) {
      return `${hours}h`
    }

    return `${hours}h ${remainingMinutes}m`
  }

  /*
   * Convert backend time such as:
   *
   * 15:00:00
   *
   * into:
   *
   * 3:00 PM
   */
  const formatShowTime = (showTime: string): string => {
    const [hoursString, minutesString] = showTime.split(':')

    const hours = Number(hoursString)
    const minutes = Number(minutesString)

    if (Number.isNaN(hours) || Number.isNaN(minutes)) {
      return showTime
    }

    const period = hours >= 12 ? 'PM' : 'AM'
    const displayHours = hours % 12 || 12
    const displayMinutes = String(minutes).padStart(2, '0')

    return `${displayHours}:${displayMinutes} ${period}`
  }

  /*
   * Save / unsave a show.
   */
  const handleToggleSave = (show: MatchingShow) => {
    const updatedSavedShows = toggleSavedShow(
      show.original,
    )

    setSavedShows(updatedSavedShows)
  }

  /*
   * Perform the actual MovieMatch search.
   */
  const performSearch = async () => {
    if (isSearching || isRefreshing) {
      return
    }

    setSearchError('')

    /*
     * Validate date.
     */
    if (!date) {
      setSearchError('Please select a date.')
      return
    }

    /*
     * Validate time.
     */
    if (!time) {
      setSearchError('Please select a time.')
      return
    }

    /*
     * Validate maximum price.
     */
    if (!maxPrice) {
      setSearchError(
        'Please select a maximum ticket price.',
      )
      return
    }

    const selectedTimeRange = timeRanges[time]

    if (!selectedTimeRange) {
      setSearchError(
        'Please select a valid time range.',
      )
      return
    }

    /*
     * Start loading only after validation succeeds.
     */
    setIsSearching(true)

    try {
      const response = await searchShows({
        location,
        date,
        start_time: selectedTimeRange.start_time,
        end_time: selectedTimeRange.end_time,
        max_price: Number(maxPrice),
      })

      const shows = convertResultsToShows(
        response.results,
      )

      setMatchingShows(shows)
      setLastUpdated('just now')
    } catch (error) {
      console.error(
        'MovieMatch search failed:',
        error,
      )

      setMatchingShows([])

      setSearchError(
        'Unable to find shows right now. Please try again.',
      )
    } finally {
      setIsSearching(false)
    }
  }

  /*
   * Refresh live availability using the same search
   * criteria currently selected by the user.
   */
const handleRefreshAvailability = async () => {
  if (isRefreshing || isSearching) {
    return
  }

  if (!date || !time || !maxPrice) {
    return
  }

  const selectedTimeRange = timeRanges[time]

  if (!selectedTimeRange) {
    return
  }

  setIsRefreshing(true)
  setSearchError('')

  try {
    const response = await searchShows({
      location,
      date,
      start_time: selectedTimeRange.start_time,
      end_time: selectedTimeRange.end_time,
      max_price: Number(maxPrice),
    })

    const shows = convertResultsToShows(
      response.results,
    )

    setMatchingShows(shows)

    const now = new Date()

    setLastUpdated(
      now.toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
      }),
    )

    /*
     * Keep the refresh state visible long enough
     * for the user to see "Refreshing...".
     */
    await new Promise((resolve) =>
      setTimeout(resolve, 700),
    )
  } catch (error) {
    console.error(
      'MovieMatch refresh failed:',
      error,
    )

    setSearchError(
      'Unable to refresh availability. Please try again.',
    )
  } finally {
    setIsRefreshing(false)
  }
}

  return (
    <div className="app">
      {/* Navbar */}
      <header className="navbar">
        <div className="navbar-container">
          <div className="logo">
            MovieMatch
          </div>

          <nav className="nav-links">
            <a href="#find-shows">
              Find Shows
            </a>

            <a href="#how-it-works">
              How It Works
            </a>

            <a href="#saved">
              Saved
            </a>
          </nav>

          <div className="nav-actions">
            <button
              type="button"
              className="login-button"
            >
              Login
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        {/* Hero Section */}
        <section
          className="hero"
          id="find-shows"
        >
          <div className="hero-content">
            <span className="hero-label">
              MOVIEMATCH
            </span>

            <h1>
              Find a movie show
              <span>
                that fits your plan.
              </span>
            </h1>

            <p>
              Choose your location, date, time and
              budget. MovieMatch finds the shows that
              match your plan.
            </p>
          </div>
        </section>

        {/* Search Panel */}
        <section className="search-section">
          <div className="search-panel">
            {/* Location */}
            <div className="search-field">
              <label htmlFor="location">
                WHERE?
              </label>

              <div className="input-wrapper">
                <span className="input-icon">
                  📍
                </span>

                <select
                  id="location"
                  value={location}
                  onChange={(event) =>
                    setLocation(event.target.value)
                  }
                >
                  <option value="Salem">
                    Salem
                  </option>

                  <option value="Chennai">
                    Chennai
                  </option>

                  <option value="Coimbatore">
                    Coimbatore
                  </option>

                  <option value="Madurai">
                    Madurai
                  </option>

                  <option value="Tiruchirappalli">
                    Tiruchirappalli
                  </option>

                  <option value="Thoothukudi">
                    Thoothukudi
                  </option>
                </select>
              </div>
            </div>

            {/* Date */}
            <div className="search-field">
              <label htmlFor="date">
                WHEN?
              </label>

              <div className="input-wrapper">
                <span className="input-icon">
                  📅
                </span>

                <input
                  id="date"
                  type="date"
                  value={date}
                  onChange={(event) =>
                    setDate(event.target.value)
                  }
                />
              </div>
            </div>

            {/* Time */}
            <div className="search-field time-field">
              <label>
                WHAT TIME?
              </label>

              <div className="time-options">
                {[
                  'Morning',
                  'Afternoon',
                  'Evening',
                  'Night',
                ].map((timeOption) => (
                  <button
                    key={timeOption}
                    type="button"
                    className={`time-button ${
                      time === timeOption
                        ? 'selected'
                        : ''
                    }`}
                    onClick={() =>
                      setTime(timeOption)
                    }
                  >
                    {timeOption}
                  </button>
                ))}
              </div>
            </div>

            {/* Maximum Ticket Price */}
            <div className="search-field price-field">
              <label>
                MAX TICKET PRICE
              </label>

              <div className="price-options">
                {[
                  '100',
                  '150',
                  '200',
                  '300',
                ].map((price) => (
                  <button
                    key={price}
                    type="button"
                    className={`price-button ${
                      maxPrice === price
                        ? 'selected'
                        : ''
                    }`}
                    onClick={() =>
                      setMaxPrice(price)
                    }
                  >
                    ₹{price}
                  </button>
                ))}
              </div>
            </div>

            {/* Search Button */}
            <div className="search-action">
              <button
                type="button"
                className="find-shows-button"
                onClick={performSearch}
                disabled={isSearching}
              >
                {isSearching
                  ? 'Finding Shows...'
                  : '🔍 Find Matching Shows'}
              </button>
            </div>
          </div>

          {/* Search Error */}
          {searchError && (
            <p className="search-error">
              {searchError}
            </p>
          )}
        </section>

        {/* Matching Shows */}
        <section className="shows-section">
          {/* Header */}
          <div className="shows-section-header">
            <div>
              <span className="section-label">
                YOUR MATCHES
              </span>

              <h2>
                Matching Shows
              </h2>

              <p>
                Shows that fit your movie plan.
              </p>
            </div>

            <span className="result-count">
              {matchingShows.length} shows
            </span>
          </div>

          {/* Availability Bar */}
          <div className="availability-bar">
            <div className="availability-info">
              <span className="availability-dot" />

              <div>
                <strong>
                  Live availability
                </strong>

                <span>
                  Updated {lastUpdated}
                </span>
              </div>
            </div>

            <button
              type="button"
              className={`refresh-button ${
                isRefreshing
                  ? 'refreshing'
                  : ''
              }`}
              onClick={handleRefreshAvailability}
              disabled={
                isRefreshing ||
                isSearching ||
                matchingShows.length === 0
              }
            >
              <span className="refresh-icon">
                ↻
              </span>

              {isRefreshing
                ? 'Refreshing...'
                : 'Refresh'}
            </button>
          </div>

{/* Show Cards */}
{matchingShows.length > 0 ? (
  <div className="show-grid">
    {matchingShows.map((show) => (
      <ShowCard
        key={`${show.movieTitle}-${show.theatre}-${show.showTime}`}
        movieTitle={show.movieTitle}
        poster={show.poster}
        language={show.language}
        format={show.format}
        duration={show.duration}
        theatre={show.theatre}
        showTime={show.showTime}
        price={show.price}
        availableSeats={show.availableSeats}
        isSaved={isShowSaved(show.original)}
        onToggleSave={() => handleToggleSave(show)}
      />
    ))}
  </div>
) : (
  <div className="empty-state no-results-state">
    <div className="empty-state-icon" aria-hidden="true">
      🎬
    </div>

    <h3>
      {searchError
        ? 'We couldn’t find your shows'
        : 'No matching shows found'}
    </h3>

    <p>
      {searchError
        ? 'Please check your connection and try searching again.'
        : 'No shows match your current movie plan. Try changing your date, time, location, or maximum ticket price.'}
    </p>
  </div>
)}

        </section>

        {/* Saved Shows */}
        <section
          className="shows-section"
          id="saved"
        >
          <div className="shows-section-header">
            <div>
              <span className="section-label">
                YOUR SAVED SHOWS
              </span>

              <h2>
                Saved
              </h2>

              <p>
                Shows you've saved for later.
              </p>
            </div>

            <span className="result-count">
              {savedShows.length} saved
            </span>
          </div>

          {savedShows.length === 0 ? (
            <div className="empty-state">
              <h3>
                No saved shows yet
              </h3>

              <p>
                Tap the heart on a matching show to
                save it here.
              </p>
            </div>
          ) : (
            <div className="show-grid">
              {savedShows.map((show) => (
                <ShowCard
                  key={show.id}
                  movieTitle={show.movie}
                  poster={show.poster_url ?? ''}
                  language={show.language}
                  format="2D"
                  duration={formatDuration(
                    show.duration_minutes,
                  )}
                  theatre={show.theatre}
                  showTime={formatShowTime(
                    show.show_time,
                  )}
                  price={show.ticket_price}
                  availableSeats={
                    show.available_seats
                  }
                  isSaved={true}
                  onToggleSave={() => {
                    const updatedSavedShows =
                      toggleSavedShow(show)

                    setSavedShows(
                      updatedSavedShows,
                    )
                  }}
                />
              ))}
            </div>
          )}
        </section>

        {/* How It Works */}
        <section
          className="how-it-works-section"
          id="how-it-works"
        >
          <div className="shows-section-header">
            <div>
              <span className="section-label">
                HOW IT WORKS
              </span>

              <h2>
                Your movie plan, simplified.
              </h2>

              <p>
                MovieMatch helps you find cinema
                shows that fit your schedule and
                budget.
              </p>
            </div>
          </div>

          <div className="how-it-works-grid">
            <div className="how-it-works-card">
              <span>01</span>

              <h3>
                Choose your plan
              </h3>

              <p>
                Select your location, date, preferred
                time and maximum ticket price.
              </p>
            </div>

            <div className="how-it-works-card">
              <span>02</span>

              <h3>
                Find matching shows
              </h3>

              <p>
                MovieMatch searches available shows
                that fit your selected preferences.
              </p>
            </div>

            <div className="how-it-works-card">
              <span>03</span>

              <h3>
                Save your favourites
              </h3>

              <p>
                Save shows you like and quickly find
                them again whenever you need them.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App