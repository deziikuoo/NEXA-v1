import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

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
        error.response?.data?.error || "Failed to fetch recommendations"
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
        error.response?.data?.error || "Failed to fetch game details"
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
