import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import requests
import asyncio
import aiohttp
from fastapi.responses import JSONResponse
import time
from datetime import datetime, timedelta
import anthropic

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Game Recommender API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class RecommendationRequest(BaseModel):
    preference: str
    sort_by: str = "release_date"
    filters: dict = {}

class GameDetailsRequest(BaseModel):
    title: str

# Function to get the Claude API key
def get_claude_api_key():
    return os.getenv('CLAUDE_API_KEY')

# Function to get the Rawg API key
def get_rawg_api_key():
    return os.getenv('RAWG_API_KEY')

# --- TWITCH API INTEGRATION ---
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_API_BASE = "https://api.twitch.tv/helix"

_twitch_token = None
_twitch_token_expiry = 0

async def get_twitch_token():
    global _twitch_token, _twitch_token_expiry
    if _twitch_token and time.time() < _twitch_token_expiry:
        return _twitch_token
    data = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(TWITCH_TOKEN_URL, data=data) as resp:
            resp.raise_for_status()
            result = await resp.json()
            _twitch_token = result["access_token"]
            _twitch_token_expiry = time.time() + result["expires_in"] - 60
            return _twitch_token

async def get_twitch_viewer_count(game_name):
    token = await get_twitch_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    # Get the game ID from Twitch
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{TWITCH_API_BASE}/games", headers=headers, params={"name": game_name}) as resp:
            data = await resp.json()
            if not data.get("data"):
                return 0
            game_id = data["data"][0]["id"]
        # Get streams for this game ID
        async with session.get(f"{TWITCH_API_BASE}/streams", headers=headers, params={"game_id": game_id, "first": 100}) as resp:
            data = await resp.json()
            if not data.get("data"):
                return 0
            return sum(stream["viewer_count"] for stream in data["data"])
# --- END TWITCH API INTEGRATION ---

# --- IGDB API INTEGRATION ---
IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID', TWITCH_CLIENT_ID)
IGDB_CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET', TWITCH_CLIENT_SECRET)
IGDB_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
IGDB_API_BASE = "https://api.igdb.com/v4"

_igdb_token = None
_igdb_token_expiry = 0

async def get_igdb_token():
    global _igdb_token, _igdb_token_expiry
    if _igdb_token and time.time() < _igdb_token_expiry:
        return _igdb_token
    data = {
        "client_id": IGDB_CLIENT_ID,
        "client_secret": IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(IGDB_TOKEN_URL, data=data) as resp:
            resp.raise_for_status()
            result = await resp.json()
            _igdb_token = result["access_token"]
            _igdb_token_expiry = time.time() + result["expires_in"] - 60
            return _igdb_token

async def igdb_search_games(query, limit=5):
    try:
        token = await get_igdb_token()
        headers = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": f"Bearer {token}",
        }
        data = f'search "{query}"; fields name,slug,first_release_date,cover.url; limit {limit};'
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{IGDB_API_BASE}/games", headers=headers, data=data) as resp:
                resp.raise_for_status()
                return await resp.json()
    except Exception as e:
        print(f"IGDB search error: {e}")
        return []

# --- END IGDB API INTEGRATION ---

# --- IGDB AUTOCOMPLETE ENDPOINT ---
@app.get("/api/igdb-autocomplete")
async def igdb_autocomplete(q: str = Query(..., min_length=1)):
    results = await igdb_search_games(q, limit=7)
    return [{"name": g["name"], "slug": g.get("slug"), "cover": g.get("cover", {}).get("url") } for g in results]
# --- END IGDB AUTOCOMPLETE ENDPOINT ---

# Enhanced filter mapping for Claude
def filters_to_natural_language(filters: dict) -> str:
    mapping = {
        "genre": "genre",
        "platform": "platform", 
        "year": "released in",
        "mode": "mode",
        "art_style": "art style",
        "perspective": "perspective",
        "difficulty": "difficulty",
        "popularity": "popularity",
        "price": "price",
        "score": "score above",
    }
    return ", ".join(f"{mapping.get(k, k)}: {v}" for k, v in filters.items() if v)

# Enhanced Claude-powered game recommendation system
async def fetch_game_titles_claude(preference: str, filters: dict = {}):
    """
    Enhanced gaming AI using Claude with specialized gaming knowledge and reasoning
    """
    claude_api_key = get_claude_api_key()
    if not claude_api_key:
        raise HTTPException(status_code=500, detail="Claude API key not found")
    
    client = anthropic.Anthropic(api_key=claude_api_key)
    
    filter_str = filters_to_natural_language(filters)
    
    # Enhanced gaming expert system prompt with trending focus
    system_prompt = """You are GameMaster AI, an elite gaming expert with comprehensive knowledge of:

GAMING EXPERTISE:
- Current gaming trends, viral hits, and what's popular in 2024-2025
- Deep understanding of modern game mechanics, design patterns, and player psychology
- Knowledge of trending games on Steam, console bestsellers, and viral indie hits
- Understanding of current gaming communities, streaming trends, and social media buzz
- Awareness of recent releases, upcoming games, and what's dominating gaming discussions
- Deep understanding of game mechanics, design patterns, and player psychology
- Knowledge of indie gems, cult classics, and hidden treasures across all platforms
RECOMMENDATION PHILOSOPHY:
- PRIORITIZE trending, popular, and widely-discussed games (80% of recommendations)
- Focus on games with active communities, high player counts, and recent buzz
- Include games that are currently popular on Twitch, YouTube, and social media
- Consider what's trending on Steam charts, console stores, and gaming platforms
- Balance with carefully selected classics and hidden gems (20% of recommendations)
- Understand the difference between games that look similar vs. games that FEEL similar

ANALYSIS DEPTH:
- Core mechanics that drive engagement (progression, challenge, discovery, creativity, social)
- Narrative themes and emotional resonance
- Art direction and atmospheric qualities
- Community aspects and multiplayer dynamics
- Platform-specific features and optimization
- Historical context and influence on the medium

RECOMMENDATION BALANCE:
- 80% POPULAR/TRENDING: Focus on what's hot, viral, and widely played right now
- 20% GEMS/CLASSICS: Include timeless classics or overlooked gems that perfectly match the request

Always prioritize what's currently popular and trending while ensuring perfect match with user preferences.
Always recommend games that truly understand what the player is seeking, not just keyword matches."""
    user_content = f"""RECOMMENDATION REQUEST:
User Interest: "{preference}"
"""
    
    if filter_str:
        user_content += f"Additional Filters: {filter_str}\n"
    
    user_content += """
TASK: Recommend exactly 18 games that match this request with optimal popularity balance.

CRITICAL REQUIREMENTS:
1. 80% TRENDING/POPULAR (14-15 games): Focus on currently popular, trending, or recently successful games
   - Games trending on Steam, Epic, console stores
   - Popular multiplayer games with active communities  
   - Recent releases (2020-2025) that gained popularity
   - Games popular on Twitch/YouTube or social media
   - Viral hits and breakthrough indie success stories

2. 20% GEMS/CLASSICS (3-4 games): Carefully selected older games or hidden gems that perfectly match
   - Timeless classics that defined their genres
   - Overlooked gems that are perfect fits for the request
   - Cult favorites with devoted followings

3. PERFECT MATCH: All games must authentically match the user's request spirit and preferences
4. CURRENT RELEVANCE: Prioritize what people are actually playing and talking about NOW
5. Return ONLY a comma-separated list of exact game titles
6. No explanations, descriptions, or extra text

FORMAT: Game Title 1, Game Title 2, Game Title 3, ...

Focus on what's HOT and TRENDING while maintaining perfect relevance to the user's preferences."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.3,  # Slight creativity while maintaining accuracy
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_content}
            ]
        )
        
        content = message.content[0].text.strip()
        # Parse the comma-separated list
        titles = [title.strip() for title in content.split(",") if title.strip()]
        
        # Clean up any potential formatting issues
        cleaned_titles = []
        for title in titles[:18]:  # Ensure max 18 titles
            # Remove any numbering, bullets, or extra formatting
            cleaned_title = title.strip()
            if cleaned_title.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.')):
                cleaned_title = cleaned_title.split('.', 1)[1].strip()
            if cleaned_title.startswith(('-', '*', '•')):
                cleaned_title = cleaned_title[1:].strip()
            if cleaned_title:
                cleaned_titles.append(cleaned_title)
        
        return cleaned_titles[:18]
        
    except Exception as e:
        print(f"Claude API error: {e}")
        # Fallback to basic recommendations if Claude fails
        return await fetch_game_titles_fallback(preference, filters)

async def fetch_game_titles_fallback(preference: str, filters: dict = {}):
    """
    Fallback recommendation system using IGDB when Claude is unavailable
    """
    try:
        # Try to get similar games from IGDB based on the preference
        igdb_results = await igdb_search_games(preference, limit=18)
        if igdb_results:
            return [game["name"] for game in igdb_results[:18]]
        else:
            # Ultimate fallback - curated list prioritizing trending/popular games (80/20 ratio)
            trending_popular_games = [
                # 80% Trending/Popular (14 games)
                "Baldur's Gate 3", "Elden Ring", "Hogwarts Legacy", "Call of Duty: Modern Warfare III",
                "Fortnite", "Apex Legends", "Valorant", "Counter-Strike 2", "Cyberpunk 2077",
                "The Witcher 3: Wild Hunt", "Grand Theft Auto V", "Red Dead Redemption 2",
                "Marvel's Spider-Man Remastered", "God of War",
                # 20% Gems/Classics (4 games)
                "Hollow Knight", "Stardew Valley", "Portal 2", "The Elder Scrolls V: Skyrim"
            ]
            return trending_popular_games
    except Exception as e:
        print(f"Fallback error: {e}")
        return ["Baldur's Gate 3", "Elden Ring", "Cyberpunk 2077", "Fortnite", "The Witcher 3: Wild Hunt"]

# Legacy function for backward compatibility (now uses Claude)
async def fetch_game_titles(preference: str, filters: dict = {}):
    """
    Main game recommendation function - now powered by Claude AI
    """
    return await fetch_game_titles_claude(preference, filters)

# Add color constants for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# RAWG API request tracking
RAWG_REQUESTS_FILE = "rawg_requests.json"
RAWG_REQUEST_LIMIT = 20000  # Monthly limit
RAWG_WARNING_THRESHOLD = 1000  # Warning when below this number

def get_monthly_stats(data):
    now = datetime.now()
    current_month = now.strftime('%Y-%m')
    monthly_requests = sum(count for date, count in data["daily_stats"].items() 
                         if date.startswith(current_month))
    return monthly_requests

def get_monthly_average(data):
    now = datetime.now()
    current_month = now.strftime('%Y-%m')
    days_in_month = now.day
    monthly_requests = get_monthly_stats(data)
    return monthly_requests / days_in_month if days_in_month > 0 else 0

def log_rawg_requests():
    data = load_rawg_requests()
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    daily_usage = data["daily_stats"].get(today, 0)
    daily_limit = RAWG_REQUEST_LIMIT // 28
    usage_color = get_color_for_usage(daily_usage, daily_limit)
    
    # Calculate daily average
    daily_avg = sum(data["daily_stats"].values()) / len(data["daily_stats"]) if data["daily_stats"] else 0
    
    # Get monthly stats
    monthly_requests = get_monthly_stats(data)
    monthly_avg = get_monthly_average(data)
    
    # Format reset time
    reset_time = datetime.fromisoformat(data["reset_time"]).strftime("%m/%d/%Y")
    
    print(f"\n[1] {Colors.BOLD}=== RAWG API Usage ==={Colors.ENDC}")
    print(f"[1]")
    print(f"[1] Daily Usage:")
    print(f"[1] Today's requests: {usage_color}{daily_usage}/{daily_limit} ({daily_usage/daily_limit*100:.1f}%){Colors.ENDC}")
    print(f"[1] Daily average requests: {daily_avg:.1f}")
    print(f"[1]")
    print(f"[1] Month's requests: {monthly_requests}")
    print(f"[1] Monthly average: {monthly_avg:.1f}")
    print(f"[1]")
    print(f"[1] Remaining requests: {data['remaining']}")
    print(f"[1] All time requests: {data['total_requests']}")
    print(f"[1]")
    print(f"[1] Reset time: {reset_time}")
    print(f"[1]")
    print(f"[1] {Colors.BOLD}====================={Colors.ENDC}\n")

def load_rawg_requests():
    if os.path.exists(RAWG_REQUESTS_FILE):
        with open(RAWG_REQUESTS_FILE, 'r') as f:
            data = json.load(f)
            # Check if reset time has passed
            reset_time = datetime.fromisoformat(data["reset_time"])
            now = datetime.now()
            if now >= reset_time:
                # Reset all stats for new cycle
                data = {
                    "remaining": RAWG_REQUEST_LIMIT,
                    "total_requests": 0,
                    "reset_time": "2025-07-16T00:00:00",  # Next reset date
                    "daily_stats": {},
                    "request_history": []
                }
                save_rawg_requests(data)
            return data
    # Initialize with current values if file doesn't exist
    initial_data = {
        "remaining": 19494,  # Current remaining requests as of March 18, 2024
        "total_requests": 506,  # Total requests made so far (20000 - 19494)
        "reset_time": "2025-07-16T00:00:00",  # Next reset date
        "daily_stats": {},
        "request_history": []
    }
    save_rawg_requests(initial_data)
    return initial_data

def save_rawg_requests(data):
    with open(RAWG_REQUESTS_FILE, 'w') as f:
        json.dump(data, f)

def update_daily_stats(data):
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in data["daily_stats"]:
        data["daily_stats"][today] = 0
    data["daily_stats"][today] += 1

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime('%m/%d/%Y %I:%M%p').lower()

def get_color_for_usage(daily_usage, daily_limit):
    percentage = (daily_usage / daily_limit) * 100
    if percentage < 70:
        return Colors.GREEN
    elif percentage < 90:
        return Colors.YELLOW
    else:
        return Colors.RED

async def fetch_game_details(titles: List[str]):
    rawg_api_key = get_rawg_api_key()
    if not rawg_api_key:
        raise HTTPException(status_code=500, detail="Rawg API key not found")

    base_url = "https://api.rawg.io/api/games"
    # Deduplicate and validate titles to avoid unnecessary API calls
    unique_titles = list(dict.fromkeys(titles))
    games = []
    
    # Load current RAWG request data
    rawg_data = load_rawg_requests()
    reset_time = datetime.fromisoformat(rawg_data["reset_time"])
    now = datetime.now()
    
    # If reset time has passed, reset the counter
    if now >= reset_time:
        rawg_data = {
            "remaining": RAWG_REQUEST_LIMIT,
            "reset_time": (now + timedelta(days=30)).isoformat(),
            "total_requests": 0,
            "daily_stats": {},
            "request_history": []
        }
        save_rawg_requests(rawg_data)

    # Track requests for this batch
    batch_requests = 0

    async def fetch_game(title):
        nonlocal batch_requests
        params = {
            "search": title,
            "key": rawg_api_key
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    response.raise_for_status()
                    # Update request counts
                    batch_requests += 1
                    rawg_data["total_requests"] += 1
                    
                    # Update daily stats
                    update_daily_stats(rawg_data)
                    
                    # Add to request history
                    rawg_data["request_history"].append({
                        "timestamp": datetime.now().isoformat(),
                        "title": title
                    })
                    
                    result = await response.json()

                    if result["results"]:
                        game = result["results"][0]
                        # Format release date
                        release_date = game.get("released", "N/A")
                        if release_date != "N/A":
                            try:
                                release_date = datetime.strptime(release_date, "%Y-%m-%d").strftime("%m/%d/%Y")
                            except ValueError:
                                pass
                        
                        # Fetch Twitch viewer count for the game title
                        viewer_count = await get_twitch_viewer_count(game["name"])
                        return {
                            "title": game["name"],
                            "release_date": release_date,
                            "platforms": ", ".join(p["platform"]["name"] for p in game.get("platforms", [])),
                            "rating": game.get("rating", "N/A"),
                            "genres": ", ".join(g["name"] for g in game.get("genres", [])),
                            "developers": ", ".join(d["name"] for d in game.get("developers", [])),
                            "metacritic": game.get("metacritic", "N/A"),
                            "background_image": game.get("background_image", ""),
                            "twitch_viewers": viewer_count
                        }
        except Exception as e:
            return None

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_game(title) for title in unique_titles]
        results = await asyncio.gather(*tasks)
        games = [game for game in results if game]
        
        # Update remaining requests after all requests are complete
        rawg_data["remaining"] -= batch_requests
        
        # Save the final state and log once after all requests are complete
        save_rawg_requests(rawg_data)
        log_rawg_requests()
        
        return games

# --- Enhanced hybrid recommendation logic ---
async def get_recommendations(preference: str, sort_by: str = "release_date", filters: dict = {}):
    """
    Enhanced recommendation system combining IGDB exact matching with Claude AI intelligence
    """
    # Try IGDB fuzzy match first for exact game titles
    igdb_results = await igdb_search_games(preference, limit=1)
    if igdb_results and igdb_results[0]["name"].lower() == preference.lower():
        # Exact match found, get this game plus similar games via Claude
        main_title = igdb_results[0]["name"]
        ai_titles = await fetch_game_titles_claude(f"Games similar to {main_title}", filters)
        titles = [main_title] + [t for t in ai_titles if t.lower() != main_title.lower()][:17]
        explain = f"Found exact match for '{main_title}' with trending games and curated gems (80% popular, 20% classics)."
    else:
        # No exact match, use Claude AI for intelligent recommendations
        titles = await fetch_game_titles_claude(preference, filters)
        explain = "Claude AI recommendations: 80% trending/popular games, 20% timeless classics - all perfectly matched to your preferences."
    
    # Fetch detailed game information
    games = await fetch_game_details(titles)
    
    if games:
        # Enhanced sorting options
        if sort_by == "rating":
            games.sort(key=lambda x: float(x["rating"]) if x["rating"] != "N/A" else 0, reverse=True)
        elif sort_by == "metacritic":
            games.sort(key=lambda x: int(x["metacritic"]) if x["metacritic"] not in ["N/A", None] else 0, reverse=True)
        else:  # release_date
            games.sort(key=lambda x: x["release_date"] if x["release_date"] != "N/A" else "1970-01-01", reverse=True)
    
    return {"games": games, "explain": explain}

async def get_game_details(title: str):
    """
    Enhanced game details with additional gaming context
    """
    rawg_api_key = get_rawg_api_key()
    if not rawg_api_key:
        raise HTTPException(status_code=500, detail="Rawg API key not found")

    base_url = "https://api.rawg.io/api/games"
    params = {
        "search": title,
        "key": rawg_api_key
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                result = await response.json()
                
                if result["results"]:
                    game = result["results"][0]
                    # Get the game ID for detailed info
                    game_id = game["id"]
                    
                    # Fetch detailed game information
                    detail_url = f"{base_url}/{game_id}"
                    async with session.get(detail_url, params={"key": rawg_api_key}) as detail_response:
                        detail_response.raise_for_status()
                        detail_result = await detail_response.json()
                        
                        # Get screenshots
                        screenshot_url = f"{base_url}/{game_id}/screenshots"
                        async with session.get(screenshot_url, params={"key": rawg_api_key}) as screenshot_response:
                            screenshot_response.raise_for_status()
                            screenshot_result = await screenshot_response.json()
                            screenshots = [s["image"] for s in screenshot_result.get("results", [])[:6]]
                        
                        return {
                            "title": detail_result["name"],
                            "description": detail_result.get("description_raw", "No description available."),
                            "screenshots": screenshots,
                            "rating": detail_result.get("rating", "N/A"),
                            "release_date": detail_result.get("released", "N/A"),
                            "platforms": ", ".join(p["platform"]["name"] for p in detail_result.get("platforms", [])),
                            "genres": ", ".join(g["name"] for g in detail_result.get("genres", [])),
                            "developers": ", ".join(d["name"] for d in detail_result.get("developers", [])),
                            "publishers": ", ".join(p["name"] for p in detail_result.get("publishers", [])),
                            "metacritic": detail_result.get("metacritic", "N/A"),
                            "esrb_rating": detail_result.get("esrb_rating", {}).get("name", "N/A") if detail_result.get("esrb_rating") else "N/A",
                            "website": detail_result.get("website", ""),
                            "background_image": detail_result.get("background_image", "")
                        }
                else:
                    raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations")
async def recommendations(request: RecommendationRequest):
    result = await get_recommendations(request.preference, request.sort_by, request.filters)
    return result

@app.post("/api/game-details")
async def game_details(request: GameDetailsRequest):
    result = await get_game_details(request.title)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 