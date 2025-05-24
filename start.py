#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles dynamic PORT environment variable properly
"""
import os
import sys
import uvicorn

# Ensure we're in the right directory and add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Change to the app directory
os.chdir(current_dir)

if __name__ == "__main__":
    # Get port from Railway environment variable, default to 8080
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'
    
    print(f"🚀 Starting ArxivChat on {host}:{port}")
    print(f"📊 Environment: PORT={port}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🐍 Python Path: {sys.path[:3]}")
    
    try:
        # Start uvicorn with Railway's port
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            workers=1,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1) 