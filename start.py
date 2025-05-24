#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles dynamic PORT environment variable properly
"""
import os
import sys
import uvicorn

# Add src to path
sys.path.insert(0, 'src')

if __name__ == "__main__":
    # Get port from Railway environment variable, default to 8080
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'
    
    print(f"🚀 Starting ArxivChat on {host}:{port}")
    print(f"📊 Environment: PORT={port}")
    
    # Start uvicorn with Railway's port
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=1,
        log_level="info"
    ) 