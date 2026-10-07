import { useState } from 'react'
import ShowCard from './components/ShowCard'

function App() {
  const [location, setLocation] = useState('Salem')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [maxPrice, setMaxPrice] = useState('')
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [lastUpdated, setLastUpdated] = useState('just now')
const matchingShows = [
  {
    movieTitle: 'Interstellar',
    poster:
      'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    language: 'English',
    format: '2D',
    duration: '2h 49m',
    theatre: 'INOX Salem',
    showTime: '2:30 PM',
    price: 120,
    availableSeats: 24,
  },
  {
    movieTitle: 'Inception',
    poster:
      'https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg',
    language: 'English',
    format: '2D',
    duration: '2h 28m',
    theatre: 'ARRS Multiplex',
    showTime: '4:15 PM',
    price: 150,
    availableSeats: 11,
  },
  {
    movieTitle: 'The Dark Knight',
    poster:
      'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
    language: 'English',
    format: 'IMAX',
    duration: '2h 32m',
    theatre: 'PVR Cinemas',
    showTime: '6:30 PM',
    price: 200,
    availableSeats: 32,
  },
  {
    movieTitle: 'The Shawshank Redemption',
    poster:
      'https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg',
    language: 'English',
    format: '2D',
    duration: '2h 22m',
    theatre: 'Sona Screens',
    showTime: '8:45 PM',
    price: 100,
    availableSeats: 7,
  },
]
const handleRefreshAvailability = () => {
  if (isRefreshing) {
    return
  }

  setIsRefreshing(true)

  setTimeout(() => {
    setLastUpdated('just now')
    setIsRefreshing(false)
  }, 900)
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
            <a href="#">Find Shows</a>
            <a href="#">How It Works</a>
            <a href="#">Saved</a>
          </nav>

          <div className="nav-actions">


            <button className="login-button">
              Login
            </button>
          </div>

        </div>
      </header>

      <main className="main-content">

        {/* Hero Section */}
        <section className="hero">
          <div className="hero-content">

            <span className="hero-label">
              MOVIEMATCH
            </span>

            <h1>
              Find a movie show
              <span>that fits your plan.</span>
            </h1>

            <p>
              Choose your location, date, time and budget.
              MovieMatch finds the shows that match your plan.
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
                <span className="input-icon">📍</span>

                <select
                  id="location"
                  value={location}
                  onChange={(event) => setLocation(event.target.value)}
                >
                  <option value="Salem">Salem</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Coimbatore">Coimbatore</option>
                  <option value="Madurai">Madurai</option>
                  <option value="Tiruchirappalli">Tiruchirappalli</option>
                  <option value="Thoothukudi">Thoothukudi</option>
                </select>
              </div>
            </div>

            {/* Date */}
            <div className="search-field">
              <label htmlFor="date">
                WHEN?
              </label>

              <div className="input-wrapper">
                <span className="input-icon">📅</span>

                <input
                  id="date"
                  type="date"
                  value={date}
                  onChange={(event) => setDate(event.target.value)}
                />
              </div>
            </div>

            {/* Time */}
            <div className="search-field time-field">
              <label>
                WHAT TIME?
              </label>

              <div className="time-options">

                {['Morning', 'Afternoon', 'Evening', 'Night'].map(
                  (timeOption) => (
                    <button
                      key={timeOption}
                      type="button"
                      className={`time-button ${
                        time === timeOption ? 'selected' : ''
                      }`}
                      onClick={() => setTime(timeOption)}
                    >
                      {timeOption}
                    </button>
                  )
                )}

              </div>
            </div>

            {/* Maximum Ticket Price */}
            <div className="search-field price-field">
              <label>
                MAX TICKET PRICE
              </label>

              <div className="price-options">

                {['100', '150', '200', '300'].map((price) => (
                  <button
                    key={price}
                    type="button"
                    className={`price-button ${
                      maxPrice === price ? 'selected' : ''
                    }`}
                    onClick={() => setMaxPrice(price)}
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
                onClick={() => {
                  console.log({
                    location,
                    date,
                    time,
                    maxPrice,
                  })
                }}
              >
                🔍 Find Matching Shows
              </button>
            </div>

          </div>

        </section>

<section className="shows-section">

  {/* Header: title on left, count on right */}
  <div className="shows-section-header">
    <div>
      <span className="section-label">YOUR MATCHES</span>
      <h2>Matching Shows</h2>
      <p>Shows that fit your movie plan.</p>
    </div>

    <span className="result-count">{matchingShows.length} shows</span>
  </div>

  {/* Availability bar now sits BELOW the header */}
  <div className="availability-bar">
    <div className="availability-info">
      <span className="availability-dot" />
      <div>
        <strong>Live availability</strong>
        <span>Updated {lastUpdated}</span>
      </div>
    </div>
    <button
      type="button"
      className={`refresh-button ${isRefreshing ? 'refreshing' : ''}`}
      onClick={handleRefreshAvailability}
      disabled={isRefreshing}
    >
      <span className="refresh-icon">↻</span>
      {isRefreshing ? 'Refreshing...' : 'Refresh'}
    </button>
  </div>

  <div className="show-grid">


    {matchingShows.map((show) => (
      <ShowCard
        key={`${show.movieTitle}-${show.theatre}-${show.showTime}`}
        {...show}
      />
    ))}

  </div>

</section>

      </main>

    </div>
  )
}

export default App