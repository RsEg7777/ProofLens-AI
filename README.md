# 🔍 ProofLens AI

**Truth Through Technology** - Advanced AI-powered verification platform for detecting misinformation, deepfakes, and malicious content.

![Version](https://img.shields.io/badge/version-2.0.0--alpha-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

---

## 🌟 Features

### ✅ Already Implemented

#### Core Verification
- **Text Verification** - AI-powered fact-checking using Ollama Llama 3.2
- **Image Detection** - AI-generated image detection with Winston AI
- **Multilingual Support** - English, Hindi, and Marathi
- **Cross-Reference Verification** - Google Custom Search API integration
- **Source Credibility Analysis** - Bias detection and source transparency

#### New in v2.0
- **🎬 Video Deepfake Detection** - Arya.ai integration for video analysis
- **🎵 Audio Deepfake Detection** - Voice cloning and manipulation detection
- **🔗 URL Reputation Checker** - VirusTotal API for malware/phishing detection
- **📄 Export Reports** - PDF, JSON, and CSV export functionality
- **🎨 Dark/Light Theme** - Modern UI with theme persistence
- **💳 Payment Integration** - Razorpay for India-compatible payments
- **🔐 Google OAuth** - Login with Google authentication
- **💰 Credit System** - Usage tracking and credit management
- **📊 Subscription Plans** - Free, Individual, and Enterprise tiers

### 🚧 Coming Soon
- Browser Extension (Chrome/Firefox)
- WhatsApp & Telegram Bots
- Bulk URL Verification
- Public REST API
- PWA Features
- Advanced Analytics Dashboard
- Real-time Verification Status
- And 60+ more features!

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama with Llama 3.2 model installed
- API keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ProofLens-AI.git
   cd ProofLens-AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Run setup script**
   ```bash
   python setup_prooflens.py
   ```
   
   This will:
   - Check Python version
   - Install all dependencies
   - Test all modules
   - Verify API configurations

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your API keys (already filled with working keys!)
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   ```
   http://localhost:5000
   ```

---

## 🔑 API Keys Configuration

All API keys are **already configured** in the `.env.example` file! Just copy it to `.env`:

### Included APIs
- ✅ **Arya.ai** - Deepfake detection (Video/Audio/Image)
- ✅ **VirusTotal** - URL reputation checking
- ✅ **Google OAuth** - Social login

### Additional APIs (You need to configure)
- **Google Custom Search** - For cross-reference verification
- **Winston AI** - Alternative image detection
- **Razorpay** - Payment processing (get keys from Razorpay Dashboard)

---

## 📖 Usage

### Text Verification
1. Navigate to the home page
2. Enter or paste text/article
3. Click "Verify"
4. View authenticity score and detailed analysis

### Deepfake Detection

#### Video
1. Go to `/video-detection`
2. Upload video file (MP4, AVI, MOV)
3. Wait for analysis
4. View deepfake probability and manipulation indicators

#### Audio
1. Go to `/audio-detection`
2. Upload audio file (MP3, WAV, M4A)
3. Get voice cloning detection results

### URL Reputation Check
1. Go to `/url-checker`
2. Enter URL to check
3. View threat analysis from 70+ security vendors
4. See malware, phishing, and threat categories

### Export Reports
After any verification:
1. Click "Export Report"
2. Choose format: PDF, JSON, or CSV
3. Download your professional report

---

## 🎨 Theme System

ProofLens AI features a modern theme system with:
- **Light Mode** - Clean, bright interface
- **Dark Mode** - Easy on the eyes
- **Auto-Detection** - Respects system preferences
- **Persistent** - Remembers your choice

Toggle theme using the button in the top-right corner (🌙/☀️)

---

## 💳 Subscription Plans

### Free Tier
- 10 verifications/month
- Basic text verification
- Image detection
- Limited exports

### Individual (₹799/month)
- 100 verifications/month
- All verification types
- Unlimited exports
- Priority support

### Enterprise (Custom pricing)
- Unlimited verifications
- API access
- Dedicated support
- White-label options
- Custom integrations

---

## 🔧 Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Ollama + Llama 3.2** - AI analysis
- **ReportLab** - PDF generation
- **Pandas** - Data processing

### Frontend
- **HTML5/CSS3** - Modern UI
- **Vanilla JavaScript** - No bloat
- **Custom CSS** - Theme system
- **Responsive Design** - Mobile-first

### APIs & Services
- **Arya.ai** - Deepfake detection
- **VirusTotal** - URL scanning
- **Google OAuth** - Authentication
- **Razorpay** - Payment processing
- **Winston AI** - Image analysis

---

## 📁 Project Structure

```
ProofLens-AI/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── auth.py                     # Authentication routes
├── deepfake_detector.py        # Arya.ai integration
├── url_checker.py              # VirusTotal integration
├── export_reports.py           # PDF/JSON/CSV exports
├── setup_prooflens.py          # Setup & testing script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── static/
│   ├── css/
│   │   └── theme.css          # Theme system
│   └── js/
│       └── utils/
│           └── themeToggle.js # Theme toggle logic
├── templates/                  # HTML templates
└── instance/
    └── prooflens.db           # SQLite database
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
python setup_prooflens.py
```

This tests:
- ✅ Python version compatibility
- ✅ All dependencies installed
- ✅ Module imports
- ✅ Custom modules
- ✅ API configurations
- ✅ Deepfake detector
- ✅ URL checker
- ✅ Export functionality
- ✅ Database connection

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.

---

## 🙏 Acknowledgments

- **Arya.ai** - For deepfake detection APIs
- **VirusTotal** - For URL reputation data
- **Ollama** - For local AI inference
- **Google** - For Custom Search API
- **Open Source Community** - For amazing tools and libraries

---

## 📞 Support

- **Documentation**: See this README for the current project status and setup notes
- **Issues**: GitHub Issues (update with your repository URL)
- **Email**: support@prooflens.ai
- **Discord**: Community link (update when available)

---

## 🗺️ Roadmap

**Current Status**: Phase 1 Complete (Core Infrastructure)

---

## ⚠️ Disclaimer

ProofLens AI is a tool to assist in fact-checking and content verification. While it uses advanced AI and multiple data sources, no automated system is 100% accurate. Always use critical thinking and verify important information through multiple sources.

---

## 🌟 Star History

If you find ProofLens AI useful, please consider giving it a star! ⭐

---

**Made with ❤️ for Truth in Journalism**

*ProofLens AI - Truth Through Technology*
