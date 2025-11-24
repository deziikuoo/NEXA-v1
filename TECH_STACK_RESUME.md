# Nexa Game Recommender - Tech Stack & Tooling Breakdown

## 1. Tech Stack

### Programming Languages
- **Python 3.9.18** - Backend development
- **JavaScript (ES6+)** - Frontend development
- **JSX** - React component syntax

### Frameworks
- **FastAPI 0.104.1** - High-performance async Python web framework
- **React 18.2.0** - Modern JavaScript UI framework with hooks
- **Uvicorn 0.24.0** - ASGI server for FastAPI production deployment

### Libraries & Dependencies

#### Backend Libraries
- **aiohttp 3.9.1** - Async HTTP client for API calls
- **Pydantic ≥2.6.0** - Data validation and serialization
- **python-dotenv 1.0.0** - Environment variable management
- **requests 2.31.0** - Synchronous HTTP library
- **openai ≥1.12.0** - OpenAI GPT-4o API integration
- **anthropic 0.40.0** - Anthropic Claude API integration
- **websockets 12.0** - WebSocket support
- **slowapi 0.1.9** - Rate limiting middleware
- **flask-cors 4.0.0** - CORS handling (legacy support)
- **Flask 3.0.0** - Legacy framework support

#### Frontend Libraries
- **axios 1.6.2** - Promise-based HTTP client
- **@headlessui/react 1.7.17** - Unstyled accessible UI components
- **@heroicons/react 2.0.18** - Icon library
- **tailwindcss 3.3.5** - Utility-first CSS framework
- **react-dom 18.2.0** - React DOM rendering

### Runtime Platforms
- **Node.js 16+** - JavaScript runtime for frontend development
- **Python 3.9.18** - Python runtime for backend
- **ASGI** - Asynchronous Server Gateway Interface (via Uvicorn)

### External APIs & Services
- **OpenAI GPT-4o** - AI-powered game recommendations
- **RAWG API** - Comprehensive game database (500,000+ titles)
- **IGDB API** - Game search and metadata
- **Twitch API** - Live streaming data and viewer counts

### Databases
- **None** - API-based architecture (no persistent database)

---

## 2. Build & Tooling

### Bundlers & Build Tools
- **react-scripts 5.0.1** - Create React App build tooling (uses Webpack under the hood)
- **npm** - Node.js package manager
- **pip** - Python package manager

### Development Tools
- **concurrently 8.2.2** - Run multiple commands simultaneously (dev dependency)
- **python-dotenv** - Environment variable management

### Linters & Code Quality
- **ESLint** - JavaScript/React linting (configured via react-app preset)
  - Extends: `react-app`, `react-app/jest`
- **Pydantic** - Runtime type checking and validation for Python

### Testing Frameworks
- **Jest** - JavaScript testing framework (via react-scripts)
- **react-scripts test** - React testing utilities

### CI/CD Tools
- **Railway** - Built-in CI/CD and deployment platform
  - Automatic builds from Git repository
  - Environment variable management
  - Health check monitoring (`/health` endpoint)
  - Auto-restart policies

### Deployment Services
- **Railway** - Primary deployment platform (full-stack)
  - Docker-based containerization
  - Automatic deployments from Git
  - Health check configuration
- **Vercel** - Frontend deployment (mentioned in README)
- **Docker** - Containerization platform
  - Multi-stage builds
  - Python 3.9-slim base image
  - Node.js and npm included

### Containerization
- **Docker** - Container orchestration
  - Dockerfile for production builds
  - Multi-stage optimization
  - Static file serving for React build

### Version Control
- **Git** - Version control system
- **GitHub** - Repository hosting (implied from README badges)

### Process Management
- **Procfile** - Process configuration for Railway/Heroku-style deployment
- **start.py** - Custom startup script for Uvicorn server

### Configuration Files
- **package.json** - Node.js dependencies and scripts
- **requirements.txt** - Python dependencies
- **tailwind.config.js** - Tailwind CSS configuration
- **railway.json** - Railway deployment configuration
- **runtime.txt** - Python version specification
- **Dockerfile** - Docker container configuration

---

## Project Architecture Summary

**Type:** Full-stack web application  
**Pattern:** RESTful API with React SPA frontend  
**Deployment:** Containerized (Docker) on Railway  
**API Architecture:** Async/await pattern with FastAPI  
**Frontend Architecture:** Component-based React with hooks  
**Styling:** Utility-first CSS (Tailwind) with custom animations


