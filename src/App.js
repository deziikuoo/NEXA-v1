import React, { useState } from "react";
import GameRecommender from "./components/GameRecommender";
import GameDetailsModal from "./components/GameDetailsModal";
import ParticlesBackground from "./components/ParticlesBackground";
import { gameService } from "./services/api";

function App() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);
  const [gameDetails, setGameDetails] = useState(null);
  const [error, setError] = useState(null);
  const [explain, setExplain] = useState("");
  const [autocomplete, setAutocomplete] = useState([]);
  const [filters, setFilters] = useState({});

  const handleGetRecommendations = async (preference, sortBy, filtersArg) => {
    setLoading(true);
    setError(null);
    try {
      const result = await gameService.getRecommendations(
        preference,
        sortBy,
        filtersArg || filters
      );
      setGames(result.games);
      setExplain(result.explain || "");
    } catch (err) {
      console.error("Error getting recommendations:", err);
      setError(
        err.message || "Failed to get recommendations. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleAutocomplete = async (query) => {
    if (!query) {
      setAutocomplete([]);
      return;
    }
    const results = await gameService.igdbAutocomplete(query);
    setAutocomplete(results);
  };

  const handleViewDetails = async (game) => {
    setSelectedGame(game);
    setLoading(true);
    setError(null);
    try {
      const details = await gameService.getGameDetails(game.title);
      setGameDetails(details);
    } catch (err) {
      console.error("Error getting game details:", err);
      setError(err.message || "Failed to get game details. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setSelectedGame(null);
    setGameDetails(null);
  };

  return (
    <div className="app-root">
      <ParticlesBackground />

      {/* Background Layers */}
      <div className="background-container">
        <div className="background-layer-back">
          <div className="neon-orb neon-orb-1"></div>
          <div className="neon-orb neon-orb-2"></div>
        </div>

        <div className="background-layer-mid">
          <div className="grid-lines"></div>
        </div>
      </div>

      <div className="main-container">
        <header className="main-header">
          <h1 className="main-title">NEXA</h1>
          <p className="main-subtitle">
            Discover your next favorite game with our advanced AI!
          </p>
          <div className="xai-badge">
            <span>🧠</span>
            Powered by GPT-4o AI Gaming Expert
          </div>
        </header>

        {error && <div className="error-message">{error}</div>}

        <GameRecommender
          onGetRecommendations={handleGetRecommendations}
          games={games}
          loading={loading}
          onViewDetails={handleViewDetails}
          error={null}
          explain={explain}
          autocomplete={autocomplete}
          onAutocomplete={handleAutocomplete}
          filters={filters}
          setFilters={setFilters}
        />

        {selectedGame && (
          <GameDetailsModal
            game={selectedGame}
            details={gameDetails}
            onClose={handleCloseModal}
            loading={loading}
          />
        )}
      </div>
    </div>
  );
}

export default App;
