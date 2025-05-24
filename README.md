# 🔬 ArxivChat - AI Research Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An intelligent research assistant that helps you search and chat about academic papers from arXiv. Built with FastAPI and enhanced with **free Gemma AI models** for comprehensive, contextual responses.

## ✨ Features

### 🔍 **Smart Paper Search**
- Real-time search through arXiv papers
- Advanced filtering and sorting options
- Paper metadata display (authors, categories, dates)

### 🤖 **Enhanced AI Chat with Gemma**
- **FREE Gemma-3n-e4b-it model** for unlimited conversations
- **Markdown-formatted responses** with rich typography
- **Context-aware explanations** combining paper content + AI knowledge
- **Educational approach** - explains concepts clearly with examples
- Smart question understanding and off-topic rejection

### 📚 **Productivity Features**
- **Bookmarking**: Save papers for later reference
- **Search History**: Track and repeat previous searches
- **Export Conversations**: Download chat sessions as JSON
- **Mobile-Responsive**: Works seamlessly on all devices

### 🚀 **Production-Ready**
- Comprehensive error handling and logging
- Health checks and monitoring endpoints
- Security headers and input validation
- Docker containerization for easy deployment

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **AI**: **Gemma-3n-e4b-it (FREE)**, Groq API, Google Gemini
- **Frontend**: Vanilla JavaScript, CSS3, Font Awesome, Marked.js
- **Deployment**: Docker, Railway.com (built-in GitHub integration)
- **CI**: GitHub Actions for testing

## 🚀 Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/avnishs17/arxivchat.git
cd arxivchat
```

### 2. **Environment Setup**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys:
GROQ_API_KEY=your_groq_api_key_here        # Optional (for Groq Gemma2)
GOOGLE_API_KEY=your_google_api_key_here    # For FREE Gemma-3n-e4b-it
LANGCHAIN_API_KEY=your_langchain_api_key   # Optional
DEBUG=true
```

### 4. **Run Locally**
```bash
python run.py
# or
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

Visit `http://localhost:8080` to start using ArxivChat!

## 🌐 Deploy to Railway

### **Automatic Deployment** ⚡
Railway has **built-in GitHub integration** - no complex CI/CD needed!

1. **Fork this repository**
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your forked ArxivChat repo
   - Railway auto-detects the Dockerfile

3. **Set Environment Variables**:
   ```bash
   GOOGLE_API_KEY=your_google_api_key    # For FREE Gemma model
   GROQ_API_KEY=your_groq_api_key       # Optional
   DEBUG=false
   ```

4. **Deploy**: Railway automatically builds and deploys!


## 🔧 Configuration

### **Environment Variables**
```bash
# Required for AI chat
GOOGLE_API_KEY=AIza...         # Google AI API for FREE Gemma-3n-e4b-it

# Optional enhancements
GROQ_API_KEY=gsk_...           # Groq API for Gemma2-9b-it
LANGCHAIN_API_KEY=lsv2_...     # LangChain tracing (optional)

# Production settings
DEBUG=false                    # Production mode
HOST=0.0.0.0                   # Server host
PORT=8080                      # Server port
```

### **API Keys Setup**

#### **Google AI API** (Primary - FREE)
1. Visit [ai.dev](https://aistudio.google.com/)
2. Generate API key for **FREE Gemma access**
3. Add to environment: `GOOGLE_API_KEY=AIza...`

#### **Groq API** (Optional Enhancement)
1. Visit [console.groq.com](https://console.groq.com)
2. Create account and generate API key
3. Add to environment: `GROQ_API_KEY=gsk_...`

## 🤖 AI Response Quality

### **What Makes Our AI Better:**
- **🆓 Completely FREE**: Uses Gemma-3n-e4b-it model at no cost
- **📖 Educational Focus**: Explains concepts clearly with examples
- **🧠 Knowledge Synthesis**: Combines paper content with broader AI knowledge
- **📝 Rich Formatting**: Markdown responses with proper typography
- **🎯 Context Aware**: Understands research domain and terminology

### **Example Response Quality:**
```markdown
**Question**: "What is the main contribution of this GNN paper?"

**AI Response**:
## Main Contribution

The primary contribution of this **Graph Neural Network** paper is the introduction of a novel **attention mechanism** that addresses the over-smoothing problem in deep GNNs.

### Key Innovations:
- **Adaptive Layer-wise Attention**: Each layer learns different attention patterns
- **Residual Connections**: Maintains node distinctiveness across layers
- **Theoretical Analysis**: Proves convergence properties mathematically

### Broader Impact:
This work builds upon *GraphSAGE* and *GAT* architectures, potentially improving:
- Node classification accuracy
- Graph representation learning
- Real-world applications like social networks and molecular modeling
```

## 🔄 CI/CD Pipeline

The project includes :
- ✅ **Code Quality**: Syntax checking and linting
- 🧪 **API Testing**: Health and endpoint validation
- 🚀 **Railway Integration**: Built-in deployment (no manual CI/CD needed)

## 📱 Usage Guide

### **Enhanced AI Conversations**
1. **Select any paper** from search results
2. **Ask detailed questions** about methodology, results, implications
3. **Get comprehensive responses** with markdown formatting
4. **Export conversations** for research notes

### **Example Questions That Work Well:**
- "Explain the methodology in detail"
- "What are the real-world applications?"
- "How does this compare to previous work?"
- "What are the limitations and future directions?"
- "Can you break down the technical concepts?"

### **Productivity Features**
- **📖 Bookmark**: Click bookmark icon on any paper
- **🕒 History**: Access previous searches from header
- **💾 Export**: Download formatted chat conversations
- **📱 Mobile**: Full functionality on mobile devices

## 🛡️ Security & Performance

- **Input Validation**: All user inputs sanitized and validated
- **Markdown Safety**: Secure rendering with XSS prevention
- **Rate Limiting**: Protection against abuse
- **Health Monitoring**: Built-in monitoring for Railway
- **Error Handling**: Graceful degradation with user feedback

## 📊 API Endpoints

### **Public Endpoints**
- `GET /` - Enhanced application interface
- `GET /api/papers?q={query}&limit={num}` - Search papers
- `POST /api/chat` - AI chat with markdown responses
- `GET /api/health` - Health check for Railway
- `GET /api/stats` - Application statistics

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Test locally**: Ensure AI responses work properly
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

## 🎉 What's New in This Version

### **🆕 Major Enhancements:**
- **FREE Gemma AI**: Switched to completely free Gemma-3n-e4b-it model
- **Markdown Responses**: Rich formatting with proper typography
- **Enhanced Prompting**: Context-aware, educational AI responses
- **Better UX**: Welcome messages, timestamps, improved loading states
- **Simplified Deployment**: Railway's built-in GitHub integration

### **🔧 Technical Improvements:**
- Enhanced LLM service with better prompt engineering
- Markdown rendering with marked.js library
- Improved error handling and user feedback
- Better mobile responsiveness
- Simplified CI/CD approach

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing open access to research papers
- [Google AI](https://ai.google/) for FREE Gemma models
- [Groq](https://groq.com/) for fast AI inference
- [Railway](https://railway.app/) for seamless deployment
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

## 📞 Support

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/avnishs17/arxivchat/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/avnishs17/arxivchat/discussions)
- **📧 Contact**: your.email@example.com

---

**Built with ❤️ for the research community - Now with FREE AI and enhanced responses!**