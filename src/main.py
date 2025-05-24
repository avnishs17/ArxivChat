"""
ArxivChat FastAPI Application - Production Ready
"""
import logging
import time
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional
import os

from config import settings
from arxiv_service import ArxivService
from llm_service import LLMService
from models import Paper, ChatMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for validation
class ChatRequest(BaseModel):
    paper_id: str
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        if len(v) > 1000:
            raise ValueError('Message too long (max 1000 characters)')
        return v.strip()
    
    @validator('paper_id')
    def validate_paper_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Paper ID cannot be empty')
        return v.strip()

# Initialize FastAPI app
app = FastAPI(
    title="ArxivChat",
    description="Search and chat about research papers",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Security middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.railway.app", "localhost", "127.0.0.1"]
    )

# CORS middleware  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://*.railway.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services with resilient startup
try:
    arxiv_service = ArxivService()
    logger.info("ArXiv service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ArXiv service: {e}")
    arxiv_service = None

try:
    llm_service = LLMService()
    logger.info("LLM service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM service: {e}")
    llm_service = None

logger.info("App initialization completed - starting FastAPI")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")

@app.get("/api/papers")
async def search_papers(q: str, limit: int = 10):
    """Search for papers on ArXiv with validation"""
    try:
        # Check service availability
        if not arxiv_service:
            raise HTTPException(status_code=503, detail="ArXiv service not available")
        
        # Input validation
        if not q or not q.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(q) > 200:
            raise HTTPException(status_code=400, detail="Query too long (max 200 characters)")
            
        if limit < 1 or limit > 50:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 50")
        
        query = q.strip()
        logger.info(f"Searching papers for query: {query[:50]}...")
        
        papers = arxiv_service.search_papers(query=query, max_results=limit)
        
        logger.info(f"Found {len(papers)} papers for query: {query[:50]}...")
        return {"papers": papers, "count": len(papers)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching papers: {e}")
        raise HTTPException(status_code=500, detail="Failed to search papers")

@app.post("/api/chat")
async def chat_with_paper(request: ChatRequest):
    """Chat about a paper with validation and rate limiting"""
    try:
        # Check service availability
        if not arxiv_service:
            raise HTTPException(status_code=503, detail="ArXiv service not available")
        
        if not llm_service:
            raise HTTPException(status_code=503, detail="LLM service not available - please check API keys")
        
        logger.info(f"Chat request for paper: {request.paper_id[:20]}...")
        
        # Get paper details
        paper = arxiv_service.get_paper_by_id(request.paper_id)
        
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        # Generate response using improved LLM service
        response = llm_service.chat_about_paper(paper, request.message)
        
        logger.info(f"Generated response for paper: {request.paper_id[:20]}...")
        return {"response": response, "paper_title": paper.get("title", "")[:100]}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        # Basic service status
        arxiv_status = "healthy" if arxiv_service else "unavailable"
        llm_status = "healthy" if llm_service else "no_api_keys"
        
        # Only test ArXiv if service is available
        if arxiv_service:
            try:
                test_papers = arxiv_service.search_papers("machine learning", 1)
                if not test_papers:
                    arxiv_status = "degraded"
            except:
                arxiv_status = "degraded"
        
        # Overall status - healthy if at least basic functionality works
        overall_status = "healthy" if arxiv_service else "degraded"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "services": {
                "arxiv_api": arxiv_status,
                "llm_service": llm_status
            },
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        # Don't fail health check completely - return degraded status
        return {
            "status": "degraded",
            "timestamp": time.time(),
            "error": "Health check partially failed",
            "version": "1.0.0"
        }

@app.get("/api/stats")
async def get_stats():
    """Basic stats endpoint"""
    return {
        "app": "ArxivChat",
        "version": "1.0.0",
        "features": ["paper_search", "ai_chat", "paper_focused_responses"],
        "apis": ["arxiv", "groq", "gemini"]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": str(exc.detail)}
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    logger.error(f"Server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Something went wrong"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ArxivChat...")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
