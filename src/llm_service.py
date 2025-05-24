"""
LLM service for chatting about papers with improved prompting
"""
import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.groq_llm = None
        self.gemini_llm = None
        
        if settings.GROQ_API_KEY:
            try:
                self.groq_llm = ChatGroq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name="gemma2-9b-it",
                    temperature=0.1,
                    max_tokens=2048
                )
                logger.info("Groq LLM initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq LLM: {e}")
        
        if settings.GOOGLE_API_KEY:
            try:
                self.gemini_llm = ChatGoogleGenerativeAI(
                    google_api_key=settings.GOOGLE_API_KEY,
                    model="gemma-3n-e4b-it",  
                    temperature=0.1
                )
                logger.info("Google Gemini LLM with Gemma-3n initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Gemini LLM: {e}")
    
    def chat_about_paper(self, paper: dict, message: str) -> str:
        """Generate enhanced responses about papers with better context and formatting"""
        try:
            context = f"""You are an expert AI research assistant with deep knowledge across scientific domains. Your task is to provide comprehensive, insightful answers about research papers by combining the paper's content with your broader scientific knowledge.

**Research Paper Context:**
- **Title**: {paper['title']}
- **Authors**: {', '.join(paper['authors'])}
- **Categories**: {', '.join(paper.get('categories', []))}
- **Abstract**: {paper['abstract']}

**Instructions for high-quality responses:**
1. **Be Comprehensive**: Provide detailed explanations, not just summaries
2. **Use Your Knowledge**: Combine paper content with your training knowledge about the field
3. **Be Educational**: Help users understand complex concepts clearly
4. **Use Markdown**: Format your response with **bold**, *italics*, bullet points, numbered lists for readability
5. **Stay Focused**: Only answer questions related to this paper or its research area
6. **Be Contextual**: Explain how this work fits into the broader research landscape

**User Question**: {message}

**Response Guidelines:**
- If about paper content/methodology/implications: Provide detailed, knowledgeable answer
- If asking for concept explanations: Relate to this paper while drawing on broader knowledge  
- If completely unrelated to research: Politely redirect to paper-related topics
- Use markdown formatting for better readability
- Provide specific examples and connections to related work when relevant

**Your comprehensive response:**"""
            
            llm = self.gemini_llm or self.groq_llm 
            
            if not llm:
                return "Sorry, no LLM service is configured. Please add your API keys."
            
            model_name = "Gemma-3n" if llm == self.gemini_llm else "Groq Gemma2"
            logger.info(f"Using {model_name} for response generation")
            
            response = llm.invoke(context)
            return self._format_response(response.content)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your question. Please try again."

    def _format_response(self, response: str) -> str:
        """Clean and format the LLM response"""
        # Remove any potential prompt leakage
        response = response.strip()
        
        # Remove prompt artifacts if they appear
        if "Instructions for high-quality responses" in response or "Response Guidelines" in response:
            lines = response.split('\n')
            cleaned_lines = []
            skip_mode = False
            
            for line in lines:
                if "Instructions" in line or "Guidelines" in line or "**Your comprehensive response:**" in line:
                    skip_mode = True
                    continue
                if skip_mode and line.strip() and not line.startswith('-') and not line.startswith('*'):
                    skip_mode = False
                if not skip_mode:
                    cleaned_lines.append(line)
            
            response = '\n'.join(cleaned_lines).strip()
        
        # Ensure we have a substantive response
        if len(response) < 50:
            return "I'd be happy to help you understand this paper better. Could you please ask a more specific question about the research methodology, findings, or implications?"
        
        return response
