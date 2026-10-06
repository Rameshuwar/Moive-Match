import './MovieCard.css'

interface MovieCardProps {
  title: string
  year: number
  rating: number
  genre: string
  poster: string
}

function MovieCard({
  title,
  year,
  rating,
  genre,
  poster,
}: MovieCardProps) {
  return (
    <article className="movie-card">
      <div className="movie-poster">
        <img src={poster} alt={title} />
      </div>

      <div className="movie-info">
        <h3>{title}</h3>

        <div className="movie-meta">
          <span>{year}</span>
          <span>⭐ {rating}</span>
        </div>

        <p>{genre}</p>
      </div>
    </article>
  )
}

export default MovieCard