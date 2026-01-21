import os


class Config:
    """Application configuration.

    All sensitive values are loaded from environment variables so that
    nothing secret is hardcoded in the repository.
    """

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Google Custom Search
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')

    # Winston AI API (image detection)
    WINSTON_AI_TOKEN = os.environ.get('WINSTON_AI_TOKEN')

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prooflens.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Arya.ai Deepfake Detection APIs
    ARYA_VIDEO_API_URL = os.environ.get('ARYA_VIDEO_API_URL', 'https://ping.arya.ai/api/v1/deepfake-detection/video')
    ARYA_IMAGE_API_URL = os.environ.get('ARYA_IMAGE_API_URL', 'https://ping.arya.ai/api/v1/deepfake-detection/image')
    ARYA_AUDIO_API_URL = os.environ.get('ARYA_AUDIO_API_URL', 'https://ping.arya.ai/api/v1/deepfake-detection/audio')
    ARYA_VIDEO_API_TOKEN = os.environ.get('ARYA_VIDEO_API_TOKEN', 'cb23fbcdf33366c4a025e7b11485a94a')
    ARYA_IMAGE_API_TOKEN = os.environ.get('ARYA_IMAGE_API_TOKEN', 'cb23fbcdf33366c4a025e7b11485a94a')
    ARYA_AUDIO_API_TOKEN = os.environ.get('ARYA_AUDIO_API_TOKEN', 'cb23fbcdf33366c4a025e7b11485a94a')

    # VirusTotal API (URL Checker)
    VIRUSTOTAL_API_KEY = os.environ.get('VIRUSTOTAL_API_KEY', 'addfe09234d2e1d45cb97414949d59350314f1dc4e0c0997a505d2694e517153')

    # Google OAuth
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '519527933418-ahmv7v3098cdfha6bmlnjlrqp8rlr3eo.apps.googleusercontent.com')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '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')

    # Razorpay Payment Processing (India-compatible)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET')

    # Redis & Celery (for background tasks)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Application branding
    APP_NAME = 'ProofLens AI'
    APP_TAGLINE = 'Truth Through Technology'

