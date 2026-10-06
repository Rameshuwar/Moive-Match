import MovieCard from './components/MovieCard'

function App() {
  return (
    <div className="app">

      <header className="navbar">
        <div className="navbar-container">

          <div className="logo">
            MovieMatch
          </div>

          <nav className="nav-links">
            <a href="#">Home</a>
            <a href="#">Discover</a>
            <a href="#">Watchlist</a>
          </nav>

          <div className="nav-actions">
            <button className="search-button">
              Search
            </button>

            <button className="login-button">
              Login
            </button>
          </div>

        </div>
      </header>

      <main className="main-content">

        <section className="hero">
          <div className="hero-content">

            <span className="hero-label">
              WELCOME TO MOVIEMATCH
            </span>

            <h1>
              Find Movies
              <br />
              You'll Love.
            </h1>

            <p>
              Discover your next favorite movie with personalized
              recommendations, ratings, and curated collections.
            </p>

            <div className="hero-actions">
              <button className="primary-button">
                Explore Movies
              </button>

              <button className="secondary-button">
                Browse Genres
              </button>
            </div>

          </div>
        </section>

        <section className="movies-section">

          <h2>Popular Movies</h2>

          <div className="movie-grid">

            <MovieCard
              title="Interstellar"
              year={2014}
              rating={8.7}
              genre="Sci-Fi"
              poster="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
            />

            <MovieCard
              title="Inception"
              year={2010}
              rating={8.8}
              genre="Sci-Fi"
              poster="https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg"
            />

            <MovieCard
              title="The Dark Knight"
              year={2008}
              rating={9.0}
              genre="Action"
              poster="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
            />

            <MovieCard
              title="The Shawshank Redemption"
              year={1994}
              rating={9.3}
              genre="Drama"
              poster="https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg"
            />

          </div>

        </section>

      </main>

    </div>
  )
}

export default App