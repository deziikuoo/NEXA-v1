import React from "react";

function GameCard({ game, onViewDetails }) {
  const formatViewerCount = (count) => {
    if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K`;
    }
    return count.toString();
  };

  return (
    <div className="game-card glass-panel">
      <div className="game-card-image">
        <img
          src={game.background_image || "https://via.placeholder.com/300x200"}
          alt={game.title}
          className="game-card-img"
        />
        {game.metacritic && game.metacritic !== "N/A" && (
          <div className="game-card-metacritic">{game.metacritic}</div>
        )}
      </div>
      <div className="game-card-content">
        <h3 className="game-card-title">{game.title}</h3>

        {game.twitch_viewers > 0 && (
          <div className="game-card-twitch-viewers">
            {formatViewerCount(game.twitch_viewers)} watching
          </div>
        )}

        <p className="game-card-info">
          <span className="game-card-label">Released:</span> {game.release_date}
        </p>
        <p className="game-card-info">
          <span className="game-card-label">Platforms:</span> {game.platforms}
        </p>
        <p className="game-card-info">
          <span className="game-card-label">Rating:</span> ⭐ {game.rating}
        </p>
        <p className="game-card-info">
          <span className="game-card-label">Genres:</span> {game.genres}
        </p>

        <button onClick={onViewDetails} className="game-card-button">
          View Details
        </button>
      </div>
    </div>
  );
}

export default GameCard;
