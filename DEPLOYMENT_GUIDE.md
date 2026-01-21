# ProofLens AI - Deployment Guide

## 🚀 Quick Deploy to Heroku

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Git repository initialized

### Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku App**
```bash
heroku create prooflens-ai
```

3. **Add PostgreSQL (Recommended for production)**
```bash
heroku addons:create heroku-postgresql:essential-0
```

4. **Set Environment Variables**
```bash
# Required
heroku config:set SECRET_KEY="your-secure-secret-key-here"
heroku config:set GOOGLE_API_KEY="your-google-api-key"
heroku config:set GOOGLE_CSE_ID="your-custom-search-engine-id"

# Optional API Keys (for full functionality)
heroku config:set WINSTON_AI_TOKEN="your-winston-ai-token"
heroku config:set VIRUSTOTAL_API_KEY="your-virustotal-key"
heroku config:set ARYA_VIDEO_API_TOKEN="your-arya-token"

# Google OAuth (for social login)
heroku config:set GOOGLE_OAUTH_CLIENT_ID="your-client-id"
heroku config:set GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"

# Razorpay (for payments)
heroku config:set RAZORPAY_KEY_ID="your-razorpay-key"
heroku config:set RAZORPAY_KEY_SECRET="your-razorpay-secret"

# Email (for contact form)
heroku config:set MAIL_USERNAME="your-email@gmail.com"
heroku config:set MAIL_PASSWORD="your-app-password"
```

5. **Deploy**
```bash
git add .
git commit -m "Production deployment"
git push heroku main
```

6. **Initialize Database**
```bash
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

7. **Open App**
```bash
heroku open
```

## 🌐 Deploy to Other Platforms

### Railway.app
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

### Render.com
1. Create new Web Service
2. Connect GitHub repository
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `gunicorn app:app`
5. Add environment variables

### DigitalOcean App Platform
1. Create new App
2. Connect GitHub repository
3. Configure environment variables
4. Deploy

## 🔧 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask secret key for sessions |
| `DATABASE_URL` | No | PostgreSQL connection URL (auto-set on Heroku) |
| `GOOGLE_API_KEY` | Yes | Google Custom Search API key |
| `GOOGLE_CSE_ID` | Yes | Google Custom Search Engine ID |
| `WINSTON_AI_TOKEN` | No | Winston AI for image detection |
| `VIRUSTOTAL_API_KEY` | No | VirusTotal API for URL checking |
| `ARYA_VIDEO_API_TOKEN` | No | Arya.ai for deepfake detection |
| `GOOGLE_OAUTH_CLIENT_ID` | No | Google OAuth client ID |
| `GOOGLE_OAUTH_CLIENT_SECRET` | No | Google OAuth client secret |
| `RAZORPAY_KEY_ID` | No | Razorpay payment key |
| `RAZORPAY_KEY_SECRET` | No | Razorpay payment secret |
| `MAIL_USERNAME` | No | SMTP email username |
| `MAIL_PASSWORD` | No | SMTP email password |

## ✅ Pre-Deployment Checklist

- [ ] All environment variables set
- [ ] Database migrations run
- [ ] Static files properly served
- [ ] HTTPS enabled
- [ ] Error pages configured
- [ ] Logging configured
- [ ] Backup strategy in place

## 📝 Post-Deployment

1. **Test all routes**
   - Homepage loads
   - Login/Signup works
   - All tool pages accessible
   - API endpoints respond

2. **Monitor**
   - Check application logs
   - Set up uptime monitoring
   - Configure error alerts

3. **Security**
   - Enable HTTPS redirect
   - Set secure cookie flags
   - Configure CORS if needed

## 🔗 Important URLs

After deployment, verify these work:
- `/` - Homepage
- `/auth/login` - Login page
- `/auth/signup` - Signup page
- `/text-verification` - Text verification tool
- `/image-detection` - Image detection tool
- `/video-detection` - Video detection tool
- `/audio-detection` - Audio detection tool
- `/url-checker` - URL checker tool
- `/pricing` - Pricing page
- `/dashboard` - User dashboard (requires login)

## 🐛 Troubleshooting

### App crashes on startup
- Check `heroku logs --tail`
- Verify all required env vars are set
- Ensure requirements.txt is complete

### Database errors
- Run `heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"`
- Check DATABASE_URL is set correctly

### Static files not loading
- Clear browser cache
- Check file paths in templates
- Ensure CSS/JS files exist

### API endpoints return 500
- Check API keys are valid
- Review application logs
- Verify request format
