#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""
import os
import uvicorn
from app_fastapi import app

if __name__ == "__main__":
    # Get port from environment variable, default to 8000
    port = int(os.getenv("PORT", 8000))

    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
