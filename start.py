#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""
import os
import sys
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting Nexa Game Recommender API...")
        
        # Get port from environment
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Using port: {port}")
        
        # Import app after logging is configured
        from app_fastapi import app
        logger.info("FastAPI app imported successfully")
        
        # Start the server
        logger.info("Starting Uvicorn server...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            workers=1,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 