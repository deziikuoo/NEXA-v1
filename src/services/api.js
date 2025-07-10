import axios from "axios";

// Automatically detect environment and use appropriate API URL
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? process.env.REACT_APP_API_URL || 'https://your-app-name.railway.app/api'
  : "http://localhost:8000/api";

console.log('API Base URL:', API_BASE_URL);

class GameService {
  async getRecommendations(preference, sortBy, filters = {}) {
    try {
      const response = await axios.post(`${API_BASE_URL}/recommendations`, {
        preference,
        sort_by: sortBy,
        filters,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || error.response?.data?.error || "Failed to fetch recommendations"
      );
    }
  }

  async getGameDetails(title) {
    try {
      const response = await axios.post(`${API_BASE_URL}/game-details`, {
        title,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || error.response?.data?.error || "Failed to fetch game details"
      );
    }
  }

  async igdbAutocomplete(query) {
    try {
      const response = await axios.get(`${API_BASE_URL}/igdb-autocomplete`, {
        params: { q: query },
      });
      return response.data;
    } catch (error) {
      return [];
    }
  }
}

export const gameService = new GameService();
