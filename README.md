# Nexa Game Recommender

A modern web application that recommends video games based on user preferences using GPT-4o AI and RAWG APIs.

## Features

- **AI-Powered Recommendations**: Uses GPT-4o to provide intelligent game suggestions
- **Multiple Data Sources**: Integrates RAWG, IGDB, and Twitch APIs for comprehensive game data
- **Smart Matching**: Finds exact game matches and provides similar recommendations
- **Real-time Data**: Includes Twitch viewer counts and current gaming trends
- **Modern UI**: React-based frontend with smooth animations and dark theme
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

### Backend
- **FastAPI** (Python) - High-performance async web framework
- **Uvicorn** - ASGI server
- **aiohttp** - Async HTTP client
- **Pydantic** - Data validation

### Frontend
- **React** - Modern JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client

### APIs
- **OpenAI GPT-4o** - AI-powered game recommendations
- **RAWG** - Game database and metadata
- **IGDB** - Game search and autocomplete
- **Twitch** - Live streaming data and viewer counts

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   RAWG_API_KEY=your_rawg_api_key
   TWITCH_CLIENT_ID=your_twitch_client_id
   TWITCH_CLIENT_SECRET=your_twitch_client_secret
   IGDB_CLIENT_ID=your_igdb_client_id
   IGDB_CLIENT_SECRET=your_igdb_client_secret
   ```

3. Start the FastAPI server:
   ```bash
   python start.py
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open your browser to `http://localhost:3000`

## Railway Deployment

The application is configured for easy deployment on Railway:

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Environment Variables**: Set the required API keys in Railway dashboard
3. **Automatic Deployment**: Railway will automatically build and deploy your app

### Required Environment Variables for Railway
- `OPENAI_API_KEY`
- `RAWG_API_KEY`
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- `IGDB_CLIENT_ID` (optional, defaults to Twitch credentials)
- `IGDB_CLIENT_SECRET` (optional, defaults to Twitch credentials)

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /api/recommendations` - Get game recommendations
- `POST /api/game-details` - Get detailed game information
- `GET /api/igdb-autocomplete` - Game search autocomplete
- `GET /api/test-gpt4o` - Test GPT-4o integration

## Usage

1. Enter your game preference (e.g., "RPG", "action games", "similar to Skyrim")
2. Select sorting options (release date, rating, Metacritic score)
3. Click "Get Recommendations" or press Enter
4. Browse through AI-curated game suggestions
5. Click on any game to view detailed information

## Architecture

The application uses a hybrid recommendation system:
- **Exact Matching**: Searches for specific games and finds similar ones
- **AI Recommendations**: GPT-4o provides intelligent suggestions based on preferences
- **Multi-Source Data**: Combines data from RAWG, IGDB, and Twitch APIs
- **Real-time Updates**: Includes current Twitch viewer counts and trending data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
