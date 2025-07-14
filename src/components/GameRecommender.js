import React, { useState } from "react";
import GameCard from "./GameCard";

function GameRecommender({
  onGetRecommendations,
  games,
  loading,
  onViewDetails,
  error,
  explain,
  autocomplete,
  onAutocomplete,
  filters,
  setFilters,
  aiDown,
  aiDownMessage,
}) {
  const [preference, setPreference] = useState("");
  const [sortBy, setSortBy] = useState("metacritic");
  const [showAutocomplete, setShowAutocomplete] = useState(false);
  const [filterChips, setFilterChips] = useState([]);
  const [promptPreview, setPromptPreview] = useState("");
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  // Placeholder filter options
  const genreOptions = [
    "Action",
    "RPG",
    "Strategy",
    "Horror",
    "Shooter",
    "Adventure",
  ];
  const platformOptions = ["PC", "PlayStation", "Xbox", "Switch", "Mobile"];
  const yearOptions = [
    "2024",
    "2023",
    "2022",
    "2021",
    "2020",
    "2010-2019",
    "2000-2009",
  ];
  const modeOptions = ["Singleplayer", "Multiplayer", "Co-op", "MMO"];
  const artStyleOptions = ["Pixel", "3D", "Cartoon", "Realistic"];
  const perspectiveOptions = ["First-person", "Third-person", "Top-down"];
  const difficultyOptions = ["Casual", "Hardcore", "Challenging"];
  const popularityOptions = ["Trending", "Hidden Gems", "Critically Acclaimed"];
  const priceOptions = ["Free", "Under $20", "$20-$40", "$40+"];
  const scoreOptions = ["80+", "70+", "60+", "Any"];

  const basicFilterOptions = [
    { key: "genre", label: "Genre", options: genreOptions },
    { key: "platform", label: "Platform", options: platformOptions },
    { key: "year", label: "Year", options: yearOptions },
    { key: "mode", label: "Mode", options: modeOptions },
  ];
  const advancedFilterOptions = [
    { key: "art_style", label: "Art Style", options: artStyleOptions },
    { key: "perspective", label: "Perspective", options: perspectiveOptions },
    { key: "difficulty", label: "Difficulty", options: difficultyOptions },
    { key: "popularity", label: "Popularity", options: popularityOptions },
    { key: "price", label: "Price", options: priceOptions },
    { key: "score", label: "Score", options: scoreOptions },
  ];

  const handleFilterChange = (filter, value) => {
    if (value) {
      // Add or update filter
      setFilters((prev) => ({ ...prev, [filter]: value }));
      if (
        !filterChips.some(
          (chip) => chip.filter === filter && chip.value === value
        )
      ) {
        setFilterChips((prev) => [...prev, { filter, value }]);
      }
    } else {
      // Remove filter if value is empty
      setFilters((prev) => {
        const newFilters = { ...prev };
        delete newFilters[filter];
        return newFilters;
      });
      setFilterChips((prev) => prev.filter((chip) => chip.filter !== filter));
    }
  };

  const handleRemoveChip = (chipToRemove) => {
    console.log('Removing chip:', chipToRemove); // Debug log
    setFilterChips((prev) => prev.filter((chip) => chip !== chipToRemove));
    setFilters((prev) => {
      const newFilters = { ...prev };
      delete newFilters[chipToRemove.filter];
      return newFilters;
    });
  };

  const handleClearAllFilters = () => {
    setFilterChips([]);
    setFilters({});
  };

  const handleSurpriseMe = () => {
    const randomGenre =
      genreOptions[Math.floor(Math.random() * genreOptions.length)];
    const randomPlatform =
      platformOptions[Math.floor(Math.random() * platformOptions.length)];
    handleFilterChange("genre", randomGenre);
    handleFilterChange("platform", randomPlatform);
  };

  React.useEffect(() => {
    // Helper to make filter string more natural
    const filterOrder = [
      "genre",
      "platform",
      "year",
      "mode",
      "art_style",
      "perspective",
      "difficulty",
      "popularity",
      "price",
      "score",
    ];
    const capFirst = (s) =>
      s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
    const filterLabels = {
      genre: (v) => `${v} games`,
      platform: (v) => `for ${v}`,
      year: (v) => `released in ${v}`,
      mode: (v) => `${capFirst(v)}`,
      art_style: (v) => `${v} art style`,
      perspective: (v) => `${v} perspective`,
      difficulty: (v) => `${capFirst(v)} difficulty`,
      popularity: (v) => `Popularity: ${v.toUpperCase()}`,
      price: (v) => `priced ${v.toUpperCase()}`,
      score: (v) => `with score above ${v}`,
    };
    let filterParts = [];
    filterOrder.forEach((key) => {
      if (filters[key]) {
        filterParts.push(filterLabels[key](filters[key]));
      }
    });
    const naturalList = (arr) => {
      if (arr.length === 0) return "";
      if (arr.length === 1) return arr[0];
      if (arr.length === 2) return `${arr[0]} and ${arr[1]}`;
      return `${arr.slice(0, -1).join(", ")}, and ${arr[arr.length - 1]}`;
    };
    let filterStr = naturalList(filterParts);
    let naturalPreview = "";
    if (filterStr && preference) {
      naturalPreview = `Showing recommendations for ${filterStr} and your interest <b>"${preference}"</b>.`;
    } else if (filterStr) {
      naturalPreview = `Showing recommendations for ${filterStr}.`;
    } else if (preference) {
      naturalPreview = `Showing recommendations for your interest <b>"${preference}"</b>.`;
    } else {
      naturalPreview = "Showing recommendations.";
    }
    setPromptPreview(naturalPreview);
  }, [filters, preference]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (preference.trim()) {
      onGetRecommendations(preference, sortBy, filters);
      setShowAutocomplete(false);
    }
  };

  const handleInputChange = (e) => {
    setPreference(e.target.value);
    if (onAutocomplete) {
      onAutocomplete(e.target.value);
      setShowAutocomplete(true);
    }
  };

  const handleSuggestionClick = (name) => {
    setPreference(name);
    setShowAutocomplete(false);
    onGetRecommendations(name, sortBy, filters);
  };

  return (
    <div>
      {/* Filter Panel - Tactical HUD */}
      <div className="filter-panel glass-panel">
        <h3>Tactical Filters</h3>
        <div className="filter-row">
          {basicFilterOptions.map(({ key, label, options }) => (
            <select
              key={key}
              onChange={(e) => handleFilterChange(key, e.target.value)}
              value={filters[key] || ""}
            >
              <option value="">
                {label}
              </option>
              {options.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          ))}
          <button
            type="button"
            className="toggle-advanced-btn"
            onClick={() => setShowAdvancedFilters((prev) => !prev)}
          >
            {showAdvancedFilters ? "−" : "+"}
          </button>
        </div>
        {showAdvancedFilters && (
          <div className="filter-row advanced">
            {advancedFilterOptions.map(({ key, label, options }) => (
              <select
                key={key}
                onChange={(e) => handleFilterChange(key, e.target.value)}
                value={filters[key] || ""}
              >
                <option value="">
                  {label}
                </option>
                {options.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            ))}
          </div>
        )}
        <div className="filter-toggle-row">
          <button
            type="button"
            className="surprise-me-btn"
            onClick={handleSurpriseMe}
          >
            🎲 Surprise Me
          </button>
        </div>
        {/* Filter Chips */}
        <div className="filter-chips">
          {filterChips.map((chip, i) => (
            <span className="filter-chip" key={chip.filter + chip.value + i}>
              {chip.filter}: {chip.value}
              <button 
                type="button" 
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  handleRemoveChip(chip);
                }}
                className="filter-chip-remove-btn"
              >
                ×
              </button>
            </span>
          ))}
          {filterChips.length > 0 && (
            <button
              type="button"
              className="clear-all-filters-btn"
              onClick={handleClearAllFilters}
            >
              Clear All
            </button>
          )}
        </div>
      </div>

      {/* Recommendation Form - AR Command Center */}
      <form onSubmit={handleSubmit} className="recommendation-form glass-panel">
        <div className="form-section">
          <label htmlFor="preference" className="form-label">
            What kind of games do you like?
          </label>
          <div className="form-row">
    
          </div>
          <div className="input-group" style={{ position: "relative" }}>
            <input
              type="text"
              id="preference"
              value={preference}
              onChange={handleInputChange}
              className="input-text"
              placeholder="Try: 'Games like Skyrim with magic and dragons' or 'Fast-paced multiplayer shooters'"
              maxLength={100}
              autoComplete="off"
              onFocus={() => setShowAutocomplete(true)}
              onBlur={() => setTimeout(() => setShowAutocomplete(false), 150)}
            />
            {showAutocomplete && autocomplete && autocomplete.length > 0 && (
              <ul className="autocomplete-dropdown">
                {autocomplete.slice(0, 7).map((s, i) => (
                  <li
                    key={s.name + i}
                    className="autocomplete-item"
                    onMouseDown={() => handleSuggestionClick(s.name)}
                  >
                    {s.cover && (
                      <img
                        src={s.cover.replace("t_thumb", "t_cover_small")}
                        alt="cover"
                      />
                    )}
                    {s.name}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="form-hint-container">
            <p className="form-hint">
              Our <span className="gpt4o-glow">GPT-4o AI</span> gaming expert understands game mechanics, player
              psychology, and gaming culture!
            </p>
          </div>
          {(preference.trim() || Object.keys(filters).length > 0) && (
            <div className="prompt-preview">
              <span dangerouslySetInnerHTML={{ __html: promptPreview }} />
            </div>
          )}
        </div>
        <div className="input-group">
          <label htmlFor="sortBy" className="form-label">
            Sort by:
          </label>
          <select
            id="sortBy"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="form-select"
          >
            <option value="release_date">Release Date</option>
            <option value="rating">Rating</option>
            <option value="metacritic">Metacritic Score</option>
          </select>
        </div>

        <button type="submit" disabled={loading} className="form-button">
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {loading && <div className="loading-spinner"></div>}

      {aiDown && (
        <div className="ai-down-message glass-panel">
          <h2>{aiDownMessage}</h2>
        </div>
      )}

      {!aiDown && explain && <div className="explain-message glass-panel">{explain}</div>}

      <div className="games-grid">
        {games.slice(0, 19).map((game, index) => (
          <GameCard
            key={game.title}
            game={game}
            onViewDetails={() => onViewDetails(game)}
          />
        ))}
      </div>
    </div>
  );
}

export default GameRecommender;
