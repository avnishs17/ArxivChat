"""
Simple configuration for ArxivChat
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging for config debugging
logger = logging.getLogger(__name__)

class Settings:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    
    # App settings
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080"))
    
    def __init__(self):
        # Log API key status (without exposing actual keys)
        logger.info(f"🔑 GROQ_API_KEY: {'✅ SET' if self.GROQ_API_KEY else '❌ MISSING'}")
        logger.info(f"🔑 GOOGLE_API_KEY: {'✅ SET' if self.GOOGLE_API_KEY else '❌ MISSING'}")
        logger.info(f"🔧 DEBUG: {self.DEBUG}")
        logger.info(f"🌍 PORT: {self.PORT}")

settings = Settings()
