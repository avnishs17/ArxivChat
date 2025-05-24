#!/usr/bin/env python3
"""
Simple run script for ArxivChat
"""
import sys
import os

# Add src to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("🚀 Starting ArxivChat...")
    print("💡 Make sure you have added your API keys to .env file!")
    print("📱 Access the app at: http://localhost:8080")
    print("⚠️  Press Ctrl+C to stop\n")
    
    try:
        import uvicorn
        # Use import string for reload to work properly
        uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
    except KeyboardInterrupt:
        print("\n👋 ArxivChat stopped!")
    except Exception as e:
        print(f"\n❌ Error starting ArxivChat: {e}")
        print("💡 Make sure you have installed requirements: pip install -r requirements.txt")
