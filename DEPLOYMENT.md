# Railway Deployment Guide

This guide will help you deploy Nexa Game Recommender to Railway without the Nix environment issues.

## Quick Fix

The deployment has been updated to use Docker instead of Nixpacks to avoid the "externally-managed-environment" error.

## Files Changed

1. **Removed**: `nixpacks.toml` (was causing Nix environment conflicts)
2. **Added**: `Dockerfile` (uses standard Python environment)
3. **Updated**: `railway.json` (now uses Docker builder)
4. **Updated**: `app_fastapi.py` (added static file serving for React app)
5. **Added**: `.dockerignore` (optimizes Docker build)

## Deployment Steps

### 1. Push Changes to GitHub
```bash
git add .
git commit -m "Fix Railway deployment: switch to Docker from Nixpacks"
git push origin main
```

### 2. Railway Configuration
1. Go to your Railway dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following environment variables:

```
OPENAI_API_KEY=your_openai_api_key
RAWG_API_KEY=your_rawg_api_key
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret
IGDB_CLIENT_ID=your_igdb_client_id (optional)
IGDB_CLIENT_SECRET=your_igdb_client_secret (optional)
```

### 3. Deploy
Railway will automatically detect the Dockerfile and build using Docker instead of Nixpacks.

## What Changed

### Before (Causing Errors)
- Used Nixpacks with Nix Python packages
- `pip install` failed due to externally managed environment
- Nix store filesystem conflicts

### After (Fixed)
- Uses Docker with standard Python 3.9-slim image
- No Nix environment conflicts
- Proper static file serving for React app
- Optimized build process

## Troubleshooting

If you still encounter issues:

1. **Check Railway Logs**: Look for specific error messages
2. **Verify Environment Variables**: Ensure all API keys are set
3. **Rebuild**: Try triggering a new deployment
4. **Contact Support**: If issues persist, contact Railway support

## API Keys Required

- **OpenAI API Key**: For GPT-4o game recommendations
- **RAWG API Key**: For game database access
- **Twitch Client ID/Secret**: For Twitch integration
- **IGDB Client ID/Secret**: For game search (optional, uses Twitch credentials as fallback)

## Health Check

The app includes a health check endpoint at `/health` that Railway uses to verify deployment success. 