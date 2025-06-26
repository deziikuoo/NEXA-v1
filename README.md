# Game Recommender Web App

A modern web application that recommends video games based on user preferences using xAI and RAWG APIs.

## Features

- Get game recommendations based on your preferences
- Sort recommendations by release date, rating, or Metacritic score
- View detailed game information including screenshots and descriptions
- Modern, responsive UI with smooth animations
- Dark theme with purple accent colors

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your API keys:
   ```
   XAI_API_KEY=your_xai_api_key
   RAWG_API_KEY=your_rawg_api_key
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter your game preference (e.g., "RPG", "action", "strategy")
2. Select how you want to sort the results
3. Click "Get Recommendations" or press Enter
4. Click on "View Details" for any game to see more information

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Styling: Tailwind CSS
- APIs: xAI, RAWG

## Note

Make sure you have valid API keys for both xAI and RAWG APIs. The application will use default keys if none are provided, but these may have limited functionality or may not work at all.
