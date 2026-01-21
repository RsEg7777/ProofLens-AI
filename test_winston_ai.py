"""
Test script for Winston AI image detection integration
Run this to verify your Winston AI token is working correctly
"""

import os
from dotenv import load_dotenv
from image_detector import ImageDetector

# Load environment variables
load_dotenv()

def test_winston_ai():
    """Test Winston AI integration with a sample image URL"""
    
    print("=" * 60)
    print("Winston AI Integration Test")
    print("=" * 60)
    
    # Get API token
    api_token = os.environ.get('WINSTON_AI_TOKEN')
    
    if not api_token:
        print("❌ ERROR: WINSTON_AI_TOKEN not found in environment")
        print("   Make sure your .env file contains the token")
        return False
    
    # Check if token looks valid (not placeholder)
    if api_token.startswith('your-') or '{{' in api_token:
        print("❌ ERROR: WINSTON_AI_TOKEN appears to be a placeholder")
        print(f"   Current value: {api_token}")
        return False
    
    print(f"✅ Token found: {api_token[:20]}...{api_token[-10:]}")
    print()
    
    # Initialize detector
    detector = ImageDetector(api_token=api_token)
    print("✅ ImageDetector initialized")
    print()
    
    # Test with a sample AI-generated image URL
    # This is a publicly available AI-generated image for testing
    test_image_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995"  # AI-generated sample
    
    print(f"🔍 Testing with image URL:")
    print(f"   {test_image_url}")
    print()
    print("⏳ Calling Winston AI API... (this may take a few seconds)")
    print()
    
    try:
        result = detector.detect_ai_image(image_url=test_image_url)
        
        if result:
            print("=" * 60)
            print("✅ SUCCESS! Winston AI API is working")
            print("=" * 60)
            print()
            print(f"📊 Detection Results:")
            print(f"   Status: {result.get('status')}")
            print(f"   AI-Generated: {result.get('is_ai_generated')}")
            print(f"   Confidence: {result.get('confidence')}%")
            print(f"   Detection Method: {result.get('detection_method')}")
            print()
            
            if 'raw_score' in result:
                print(f"   Raw Score: {result.get('raw_score')}/100")
            
            if result.get('has_watermark'):
                print(f"   Watermark Detected: Yes")
                print(f"   Issuers: {', '.join(result.get('watermark_issuers', []))}")
            else:
                print(f"   Watermark Detected: No")
            
            print()
            print("📝 Reasons:")
            for i, reason in enumerate(result.get('reasons', []), 1):
                print(f"   {i}. {reason}")
            
            print()
            if 'credits_used' in result:
                print(f"💳 Credits:")
                print(f"   Used: {result.get('credits_used')}")
                print(f"   Remaining: {result.get('credits_remaining')}")
            
            print()
            print("=" * 60)
            print("🎉 Winston AI integration is fully functional!")
            print("=" * 60)
            return True
        else:
            print("❌ ERROR: No result returned from API")
            print("   Check console output above for error messages")
            return False
            
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR: Exception occurred during test")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check your internet connection")
        print("   2. Verify your Winston AI token is valid")
        print("   3. Check if you have remaining credits")
        print("   4. Review WINSTON_AI_SETUP.md for more help")
        return False

if __name__ == "__main__":
    success = test_winston_ai()
    exit(0 if success else 1)
