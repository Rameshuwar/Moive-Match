import './ShowCard.css'

interface ShowCardProps {
  movieTitle: string
  poster: string
  language: string
  format: string
  duration: string
  theatre: string
  showTime: string
  price: number
  availableSeats: number
  isSaved: boolean
  onToggleSave: () => void
}

function ShowCard({
  movieTitle,
  poster,
  language,
  format,
  duration,
  theatre,
  showTime,
  price,
  availableSeats,
  isSaved,
  onToggleSave,
}: ShowCardProps) {
  return (
    <article className="show-card">
      <div className="show-card-poster">
        <img
          src={poster}
          alt={`${movieTitle} poster`}
        />
      </div>

      <div className="show-card-content">
        <div className="show-card-header">
          <h3>{movieTitle}</h3>

          <button
            type="button"
            className={`save-show-button ${
              isSaved ? 'saved' : ''
            }`}
            aria-label={
              isSaved
                ? `Remove ${movieTitle} from saved shows`
                : `Save ${movieTitle}`
            }
            aria-pressed={isSaved}
            onClick={onToggleSave}
          >
            {isSaved ? '♥' : '♡'}
          </button>
        </div>

        <div className="show-meta">
          <span>{language}</span>
          <span>•</span>
          <span>{format}</span>
          <span>•</span>
          <span>{duration}</span>
        </div>

        <div className="show-details">
          <div className="show-detail">
            <span className="detail-label">THEATRE</span>
            <span className="detail-value">{theatre}</span>
          </div>

          <div className="show-detail">
            <span className="detail-label">SHOW TIME</span>
            <span className="detail-value show-time">
              {showTime}
            </span>
          </div>
        </div>

        <div className="show-card-footer">
          <div className="ticket-price">
            <span className="price-label">TICKET</span>
            <strong>₹{price}</strong>
          </div>

          <div
            className={`seat-status ${
              availableSeats <= 10 ? 'low' : ''
            }`}
          >
            <span className="status-dot" />

            <span>
              {availableSeats} seats available
            </span>
          </div>
        </div>
      </div>
    </article>
  )
}

export default ShowCard