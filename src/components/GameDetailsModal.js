import React from "react";

function GameDetailsModal({ game, details, onClose, loading }) {
  if (!game) return null;

  return (
    <div className="modal-root">
      <div className="modal-overlay" onClick={onClose} />
      <div className="modal-content glass-panel">
        <div className="modal-header">
          <h2 className="modal-title">{game.title}</h2>
          <button onClick={onClose} className="modal-close">
            ×
          </button>
        </div>

        {loading ? (
          <div className="modal-loading">
            <div className="loading-spinner"></div>
          </div>
        ) : details ? (
          <>
            {details.screenshots && details.screenshots.length > 0 && (
              <div className="modal-screenshots">
                {details.screenshots.map((screenshot, index) => (
                  <img
                    key={index}
                    src={screenshot}
                    alt={`${game.title} screenshot ${index + 1}`}
                    className="modal-screenshot-img"
                  />
                ))}
              </div>
            )}

            <div className="modal-description">
              <p>{details.description || "No description available."}</p>
            </div>

            <div className="modal-info">
              <p className="game-card-info">
                <span className="game-card-label">Released:</span>{" "}
                {game.release_date}
              </p>
              <p className="game-card-info">
                <span className="game-card-label">Platforms:</span>{" "}
                {game.platforms}
              </p>
              <p className="game-card-info">
                <span className="game-card-label">Rating:</span> ⭐{" "}
                {game.rating}
              </p>
              <p className="game-card-info">
                <span className="game-card-label">Genres:</span> {game.genres}
              </p>
              <p className="game-card-info">
                <span className="game-card-label">Developers:</span>{" "}
                {game.developers}
              </p>
              {game.metacritic && game.metacritic !== "N/A" && (
                <p className="game-card-info">
                  <span className="game-card-label">Metacritic:</span>{" "}
                  {game.metacritic}
                </p>
              )}
            </div>

            {details.website && (
              <p className="game-card-info">
                <span className="game-card-label">Website:</span>{" "}
                <a
                  href={details.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="modal-link"
                >
                  {details.website}
                </a>
              </p>
            )}
          </>
        ) : (
          <p className="modal-no-details">No additional details available.</p>
        )}
      </div>
    </div>
  );
}

export default GameDetailsModal;
