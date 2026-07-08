# ProofLens AI

ProofLens AI is a Flask-based misinformation and media verification platform. It combines local LLM analysis, source cross-checking, AI image detection, media deepfake checks, URL reputation scanning, user accounts, credit tracking, subscriptions, and exportable verification reports.

The project is built for experimentation around content authenticity. It is not a replacement for professional fact-checking, security review, or editorial judgment.

## Core Features

- Text and news verification using Ollama with Llama 3.2.
- Claim extraction, source discovery, and cross-reference checks through Google Custom Search.
- Image AI-generation detection with Winston AI, plus local metadata and artifact fallback checks.
- Meme and quote verification support with OCR when Tesseract is installed.
- Video and audio deepfake detection through Arya.ai API integrations.
- URL reputation checks through VirusTotal.
- English, Hindi, and Marathi language detection and translation support.
- User authentication, Google OAuth, profile pages, verification history, and saved articles.
- Credit-based usage tracking for protected verification tools.
- Subscription plans and Razorpay payment flow.
- Exportable verification reports in PDF, JSON, and CSV.
- Responsive Flask/Jinja frontend with reusable components and theme assets.

## Tech Stack

- Backend: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail
- AI and verification: Ollama, Google Custom Search, Winston AI, Arya.ai, VirusTotal
- Data extraction: BeautifulSoup, trafilatura
- Image and OCR: Pillow, OpenCV, pytesseract
- Reports: ReportLab, pandas
- Payments and auth: Razorpay, Google OAuth
- Deployment: Gunicorn, Procfile, `runtime.txt`

## Project Structure

```text
ProofLens-AI/
|-- app.py                  # Main Flask app and verification routes
|-- auth.py                 # Login, signup, profile, Google OAuth
|-- config.py               # Environment-based configuration
|-- models.py               # SQLAlchemy models
|-- credit_utils.py         # Credit checks and usage accounting
|-- deepfake_detector.py    # Arya.ai video/audio/image deepfake clients
|-- image_detector.py       # Winston AI image detection and local fallback
|-- url_checker.py          # VirusTotal URL reputation checker
|-- export_reports.py       # PDF, JSON, and CSV report generation
|-- payment_handler.py      # Razorpay subscription handling
|-- init_database.py        # Database and subscription-plan bootstrap
|-- templates/              # Jinja pages and components
|-- static/                 # CSS, JavaScript, and image assets
|-- requirements.txt        # Python dependencies
|-- Procfile                # Production web command
`-- runtime.txt             # Python runtime for deployment
```

## Requirements

- Python 3.8 or newer. The deployment runtime currently targets Python 3.11.7.
- Ollama installed locally with the `llama3.2` model available.
- API credentials for the services you want to use.
- Optional: Tesseract OCR for meme and quote image text extraction.

Install the Ollama model:

```bash
ollama pull llama3.2
```

On Windows, OCR support expects Tesseract at:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/soham-dev77/ProofLens-AI.git
cd ProofLens-AI
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` with your own service credentials. Do not commit real secrets.

Initialize the database and default subscription plans:

```bash
python init_database.py
```

Run the app:

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

## Environment Variables

Set only the integrations you need for your local workflow. Text/news verification needs Google Custom Search and Ollama. Image, video, audio, payments, OAuth, and URL checks need their respective external credentials.

```text
SECRET_KEY
DATABASE_URL
GOOGLE_API_KEY
GOOGLE_CSE_ID
WINSTON_AI_TOKEN
ARYA_VIDEO_API_URL
ARYA_IMAGE_API_URL
ARYA_AUDIO_API_URL
ARYA_VIDEO_API_TOKEN
ARYA_IMAGE_API_TOKEN
ARYA_AUDIO_API_TOKEN
VIRUSTOTAL_API_KEY
GOOGLE_OAUTH_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET
RAZORPAY_WEBHOOK_SECRET
MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USE_SSL
MAIL_USERNAME
MAIL_PASSWORD
REDIS_URL
CELERY_BROKER_URL
CELERY_RESULT_BACKEND
```

## Main Routes

```text
/                       Home
/text-verification      Text verification UI
/news-verification      News verification UI
/image-detection        AI image detection UI
/video-detection        Video deepfake detection UI
/audio-detection        Audio deepfake detection UI
/url-checker            URL reputation checker UI
/pricing                Subscription plans
/dashboard              User dashboard
/auth/login             Login
/auth/signup            Signup
/auth/profile           Profile
```

Important JSON and upload endpoints include:

```text
POST /verify_text
POST /verify_meme
POST /detect_image
POST /detect_video
POST /detect_audio
POST /check_url
POST /detect_language
POST /translate
GET  /export/<format>/<verification_id>
```

## Verification Workflow

1. A user submits text, an article, a URL, or media.
2. ProofLens extracts claims or file metadata depending on the tool.
3. Text and news flows use Ollama for analysis and Google Custom Search for external source discovery.
4. Media flows call the configured detection service and fall back where local analysis is available.
5. Results are scored, explained, and stored for authenticated users.
6. Users can review history, save articles, spend credits, and export reports.

## Testing And Health Checks

Run the setup verification script:

```bash
python setup_prooflens.py
```

The script checks Python compatibility, installs requirements, imports key modules, validates configuration availability, exercises report export generation, and checks for a local database.

You can also test the Winston AI integration separately:

```bash
python test_winston_ai.py
```

## Deployment

The repository includes:

- `Procfile` for Gunicorn-based hosting.
- `runtime.txt` for Python runtime selection.
- `DEPLOYMENT_GUIDE.md` with Heroku, Railway, Render, and DigitalOcean notes.

Typical production command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

For production, use a real `SECRET_KEY`, configure all required environment variables in the hosting provider, and prefer a managed PostgreSQL database through `DATABASE_URL`.

## Security Notes

- Keep `.env` local and out of Git.
- Rotate any API keys that were ever committed or shared.
- Do not rely on sample or default credentials for production.
- Use HTTPS in production, especially for login, OAuth callbacks, payments, and report downloads.
- Treat automated authenticity scores as decision support, not final proof.

## License

This project is licensed under the MIT License. See [LICENCE](LICENCE) for details.
