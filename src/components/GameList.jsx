import React from "react";
import { motion } from "framer-motion";
import {
  FaTwitch,
  FaStar,
  FaCalendarAlt,
  FaGamepad,
  FaUsers,
  FaCode,
  FaTrophy,
} from "react-icons/fa";

const GameCard = ({ game }) => {
  const [isHovered, setIsHovered] = React.useState(false);
  const [showDetails, setShowDetails] = React.useState(false);
  const [details, setDetails] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  const handleClick = async () => {
    if (!showDetails && !details) {
      setIsLoading(true);
      try {
        const response = await fetch("/api/game-details", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ title: game.title }),
        });
        const data = await response.json();
        setDetails(data);
      } catch (error) {
        console.error("Error fetching game details:", error);
      } finally {
        setIsLoading(false);
      }
    }
    setShowDetails(!showDetails);
  };

  return (
    <motion.div
      className="bg-white rounded-lg shadow-lg overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      style={{ cursor: "pointer" }}
    >
      <div className="relative">
        <img
          src={
            game.background_image ||
            "https://via.placeholder.com/400x225?text=No+Image"
          }
          alt={game.title}
          className="w-full h-48 object-cover"
        />
        {isHovered && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="text-white text-lg font-semibold">
              Click for more details
            </span>
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="text-xl font-bold mb-2">{game.title}</h3>
        <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
          <div className="flex items-center">
            <FaCalendarAlt className="mr-1" />
            <span>{game.release_date}</span>
          </div>
          <div className="flex items-center">
            <FaGamepad className="mr-1" />
            <span>{game.platforms}</span>
          </div>
          <div className="flex items-center">
            <FaStar className="mr-1" />
            <span>{game.rating}/5</span>
          </div>
          <div className="flex items-center">
            <FaUsers className="mr-1" />
            <span>{game.genres}</span>
          </div>
          <div className="flex items-center">
            <FaCode className="mr-1" />
            <span>{game.developers}</span>
          </div>
          <div className="flex items-center">
            <FaTrophy className="mr-1" />
            <span>{game.metacritic || "N/A"}</span>
          </div>
          <div className="flex items-center">
            <FaTwitch className="mr-1" />
            <span>{game.twitch_viewers} viewers</span>
          </div>
        </div>
        {showDetails && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            {isLoading ? (
              <div className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ) : details ? (
              <>
                <p className="text-sm text-gray-700 mb-2">
                  {details.description}
                </p>
                <div className="grid grid-cols-3 gap-2">
                  {details.screenshots.map((screenshot, index) => (
                    <img
                      key={index}
                      src={screenshot}
                      alt={`Screenshot ${index + 1}`}
                      className="w-full h-20 object-cover rounded"
                    />
                  ))}
                </div>
                {details.website && (
                  <a
                    href={details.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline text-sm mt-2 inline-block"
                  >
                    Visit Website
                  </a>
                )}
              </>
            ) : (
              <p className="text-sm text-gray-500">
                No additional details available.
              </p>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};

const GameList = ({ games, explain }) => {
  if (!games || games.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">
          No games found. Try a different search term.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <p className="text-sm text-gray-600 italic">{explain}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {games.map((game, index) => (
          <GameCard key={index} game={game} />
        ))}
      </div>
    </div>
  );
};

export default GameList;
