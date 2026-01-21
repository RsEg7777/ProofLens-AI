# Winston AI Integration Guide

## Overview
VerifAI now uses Winston AI API for AI-generated image detection, replacing the previous SightEngine integration.

## Why Winston AI?
- **98%+ accuracy** in detecting AI-generated images
- Detects images from all major AI tools: Midjourney, DALL-E, Stable Diffusion, Adobe Firefly, Meta AI, and more
- **Watermark detection**: Checks for C2PA and IPTC AI watermarks
- **Comprehensive metadata analysis**: Provides detailed forensics on image origin
- **No false positives**: Trained on the largest human-reviewed dataset

## Getting Started

### 1. Create Winston AI Account
1. Visit https://app.gowinston.ai/register
2. Sign up for a free account (no credit card required)
3. You'll receive **2,000 free credits** to get started

### 2. Generate API Token
1. Log in to your Winston AI dashboard
2. Navigate to **API** section
3. Click **Generate Token** or copy your existing token
4. Keep this token secure - it's your authentication key

### 3. Configure VerifAI
1. Copy `.env.example` to `.env` if you haven't already:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your Winston AI token:
   ```
   WINSTON_AI_TOKEN=your-actual-token-here
   ```

3. Restart the application:
   ```powershell
   python app.py
   ```

## API Usage & Costs

### Credit System
- **Cost**: 300 credits per image analysis
- **Free tier**: 2,000 credits (enough for ~6-7 image detections)
- **Paid plans**: 
  - Essential: $18/month (80,000 words worth of credits)
  - Advanced: $29/month (200,000 words worth of credits)

### Rate Limits
- Standard: 500 requests per minute
- Higher limits available upon request

## Features

### What Winston AI Detects
✅ AI-generated images from:
- Midjourney
- DALL-E (all versions)
- Stable Diffusion
- Adobe Firefly
- Meta AI
- Bing Image Creator
- Ideogram
- And more...

✅ Deepfakes
✅ AI watermarks (C2PA, IPTC)
✅ Image metadata forensics

### Response Format
Winston AI returns:
- **Score**: 0-100 (higher = more likely AI-generated)
- **is_ai_generated**: Boolean determination
- **has_watermark**: Whether AI watermarks were detected
- **watermark_issuers**: List of detected watermark sources
- **metadata**: Complete forensic analysis
- **credits_used** & **credits_remaining**: Track your usage

## Fallback Behavior

If Winston AI token is not configured or credits run out:
- VerifAI falls back to **local metadata analysis**
- Uses EXIF data, dimension patterns, and software signatures
- **Lower accuracy** but still provides useful insights
- A note will appear indicating API is unavailable

## Testing Your Integration

### Test with Sample Image
1. Navigate to http://localhost:5000/image-detection
2. Upload a test image
3. Check the console output for Winston AI API calls:
   ```
   Calling Winston AI API with base64 image...
   Winston AI Response Status: 200
   Winston AI Response: {...}
   ```

### Verify Credits
The detection result will include:
```json
{
  "credits_used": 300,
  "credits_remaining": 1700
}
```

Monitor your remaining credits to know when to purchase more.

## API Documentation
- Main docs: https://docs.gowinston.ai/
- Image detection: https://docs.gowinston.ai/api-reference/v2/image-detection/post
- Dashboard: https://app.gowinston.ai/

## Support
- Winston AI support: https://gowinston.ai/
- VerifAI issues: Check WARP.md for common pitfalls

## Migration Notes (from SightEngine)

### What Changed
- `SIGHTENGINE_API_USER` & `SIGHTENGINE_API_SECRET` → `WINSTON_AI_TOKEN`
- `ImageDetector(api_user, api_secret)` → `ImageDetector(api_token)`
- Response format updated to Winston AI's structure
- Added watermark detection support
- Improved accuracy and detection capabilities

### What Stayed the Same
- Fallback local analysis still works
- API call flow unchanged (detect → parse → display)
- Database storage format compatible
- User experience identical

## Troubleshooting

### "Winston AI: Invalid or missing authentication token"
- Check your `.env` file has `WINSTON_AI_TOKEN` set
- Verify token is copied correctly (no extra spaces)
- Ensure token hasn't expired (regenerate if needed)

### "Winston AI: Insufficient credits"
- Purchase more credits at https://app.gowinston.ai/
- Use local fallback temporarily
- Monitor usage via credits_remaining in response

### "Winston AI: Request timeout"
- Large images may take longer to process
- Default timeout is 60 seconds
- Check your internet connection
- Try again with a smaller image

### Local Analysis Fallback Activated
- Configure `WINSTON_AI_TOKEN` in `.env` for best accuracy
- Local analysis uses metadata only (less reliable)
- Purchase Winston AI credits for production use
