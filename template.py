import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "arxiv_chat"

# SIMPLE ArxivChat structure - Minimal Viable Project
# Just the absolute essentials to get started
list_of_files = [
    # Basic Python files
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",
    
    # Simple backend (FastAPI)
    "src/__init__.py",
    "src/main.py",
    "src/config.py",
    "src/arxiv_service.py",
    "src/llm_service.py",
    "src/models.py",
    
    # Basic frontend (optional - can be added later)
    "static/index.html",
    "static/style.css",
    "static/script.js",
    
    # Run script
    "run.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

print("\n🎉 Simple ArxivChat project created!")
print("\n📁 Project structure:")
print("├── src/           # Backend code (FastAPI)")
print("├── static/        # Simple frontend (HTML/CSS/JS)")
print("├── tests/         # Basic tests")
print("├── requirements.txt")
print("├── .env.example")
print("└── run.py         # Start the app")
print("\n✨ Features:")
print("✅ FastAPI backend")
print("✅ ArXiv paper search")
print("✅ LLM chat integration")
print("✅ Simple HTML frontend")
print("✅ Easy to expand")
print("\n🚀 Next steps:")
print("1. pip install -r requirements.txt")
print("2. Add your API keys to .env")
print("3. python run.py")
print("4. Visit http://localhost:8000")
