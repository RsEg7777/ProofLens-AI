# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

NewsGuard AI (VerifAI) is a Flask-based news verification platform that uses AI to analyze and verify the authenticity of news articles and images. The system cross-references content against trusted sources and provides detailed authenticity scores.

## Development Commands

### Environment Setup
```powershell
# Create and activate virtual environment
python -m venv env
.\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py
```

### Running the Application
```powershell
# Development server
python app.py

# Production server with Gunicorn (not typically used on Windows)
gunicorn wsgi:app
```

### Configuration
- Copy `.env.example` to `.env` and configure environment variables
- Required: `GOOGLE_API_KEY`, `GOOGLE_CSE_ID` for news verification
- Optional: `WINSTON_AI_TOKEN` for AI image detection (300 credits per image)
- Optional: Email settings for contact form functionality

### Database Management
- Database is SQLite by default (`newsguard.db`)
- No migration system in place - changes to `models.py` require manual schema updates or `init_db.py` re-run
- For PostgreSQL, update `DATABASE_URL` in environment variables

## Architecture

### Core Components

**app.py** - Main Flask application with routes for:
- News article verification workflow (extract → analyze → cross-check → score)
- Image detection and analysis
- User dashboard and history tracking
- Contact form and static pages

**auth.py** - Authentication blueprint handling:
- User registration/login/logout
- Profile management
- User-specific features (history, saved articles)

**models.py** - SQLAlchemy database models:
- `User` - User accounts with Flask-Login integration
- `UserHistory` - Activity tracking for logged-in users
- `SavedArticle` - User-saved articles for reference
- `VerificationResult` - Stored verification scores and findings
- `SearchQuery` - Search history tracking
- `ImageDetectionResult` - Image analysis results

**image_detector.py** - AI image detection using:
- Winston AI API for AI-generated image detection with 98%+ accuracy
- Detects images from Midjourney, DALL-E, Stable Diffusion, Adobe Firefly, Meta AI, and more
- Checks for AI watermarks (C2PA, IPTC metadata)
- Local fallback using EXIF metadata analysis
- OCR support (pytesseract) for meme/quote detection

**source_data.py** - News source transparency data:
- Bias labels (left, center-left, center, center-right, right)
- Credibility scores (high, medium, low)
- Source descriptions for major news outlets

**config.py** - Centralized configuration loading from environment variables

### AI/ML Integration

**Ollama with Llama 3.2** - Local LLM for:
- Extracting key points from news articles
- Analyzing authenticity and cross-referencing sources
- Generating detailed verification reports with scores

**Google Custom Search API** - For finding trusted sources to cross-reference news claims

### Optional Features

**Multilingual Support** (requires langdetect + deep-translator):
- Detects article language
- Translates to English for verification
- Supports English, Hindi, Marathi

**OCR Meme Detection** (requires pytesseract + opencv-python):
- Extracts text from images for verification
- Requires Tesseract-OCR installed on Windows at `C:\Program Files\Tesseract-OCR\tesseract.exe`

### Frontend Structure

- `templates/` - Jinja2 templates with Bootstrap styling
  - `auth/` - Authentication pages (login, signup, profile)
  - `components/` - Reusable template components
  - Main pages: index, text_verification, image_detection, search_results
- `static/` - CSS, JS, and images
  - `js/` - Frontend JavaScript for interactive features
  - `css/` - Custom styling

## Key Workflows

### Text Verification Flow
1. User submits article text or URL
2. Extract article content (using trafilatura/BeautifulSoup)
3. Ollama extracts key claims/headlines
4. Google Search finds related trusted sources
5. Ollama cross-references and generates authenticity score
6. Results stored in database (if user is logged in)

### Image Detection Flow
1. User uploads image file
2. Check SightEngine API for AI-generation detection
3. Fallback to EXIF metadata analysis if API unavailable
4. Optional OCR to extract text from memes/quotes
5. Provide confidence score and detailed analysis

## Important Notes

- **No test suite exists** - manual testing is required
- **No linting/formatting configuration** - follow existing code style
- **Database migrations not automated** - schema changes require manual handling
- **Ollama must be running locally** with Llama 3.2 model available
- **API keys required** for core functionality (Google Custom Search)
- **Winston AI token optional** but recommended for accurate image detection (costs 300 credits per image)
- **Windows-specific paths** hardcoded for Tesseract OCR

## Common Pitfalls

- Forgetting to activate virtual environment before running
- Missing `.env` file causes application to use default/missing API keys
- Ollama not running results in verification failures
- Database file permissions on Windows can cause SQLite errors
- Winston AI API rate limits (insufficient credits) affect image detection availability
- Image detection fallback to local analysis (metadata only) has lower accuracy

## Development Guidelines

- Authentication uses Flask-Login with session management
- All user actions logged to `UserHistory` when authenticated
- Use `@login_required` decorator for protected routes
- Database queries use SQLAlchemy ORM
- Frontend uses vanilla JavaScript with fetch API
- Configuration loaded exclusively from environment variables via `config.py`
