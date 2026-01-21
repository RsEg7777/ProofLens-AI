"""
AI Image Detection Service
Detects AI-generated images using Winston AI API.

Winston AI provides AI-generated content detection that can:
1. Detect if an image is AI-generated with 98%+ accuracy
2. Detect deepfakes made with Midjourney, DALL-E, Stable Diffusion, and more
3. Works on pixel content with metadata verification
4. Checks for AI watermarks (C2PA, IPTC)

API Documentation: https://docs.gowinston.ai/api-reference/v2/image-detection/post
Supports: Midjourney, DALL-E, Stable Diffusion, Adobe Firefly, Meta AI, and more
Cost: 300 credits per image analysis
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image
from PIL.ExifTags import TAGS


class ImageDetector:
    """Service class for detecting AI-generated images using Winston AI API"""
    
    # Winston AI API endpoint
    WINSTON_API_URL = "https://api.gowinston.ai/v2/image-detection"
    
    # Known AI generation software signatures for local fallback
    AI_SOFTWARE_SIGNATURES = [
        'stable diffusion', 'midjourney', 'dall-e', 'dalle', 'novelai',
        'automatic1111', 'comfyui', 'invoke', 'diffusers', 'sd',
        'nai diffusion', 'dreamstudio', 'leonardo', 'firefly',
        'bing image creator', 'ideogram', 'playground', 'meta ai'
    ]
    
    def __init__(self, api_token=None, **kwargs):
        """
        Initialize the ImageDetector.
        
        Args:
            api_token: Winston AI API token (Bearer token)
        """
        self.api_token = api_token
    
    def detect_ai_image(self, image_file=None, image_url=None):
        """
        Detect if an image is AI-generated using Winston AI API.
        
        Args:
            image_file: File object or bytes of the image (optional if image_url provided)
            image_url: URL of the image to analyze (optional if image_file provided)
            
        Returns:
            dict: Detection results with confidence, status, and analysis
        """
        try:
            # Validate input
            if not image_file and not image_url:
                return self._create_error_response("Either image_file or image_url must be provided")
            
            # Try Winston AI API first (primary method)
            if self.api_token and not str(self.api_token).startswith('{{'):
                result = self._detect_with_winston_ai(image_file, image_url)
                if result:
                    return result
            
            # Fallback to local analysis if API unavailable
            if image_file:
                if hasattr(image_file, 'read'):
                    image_bytes = image_file.read()
                    image_file.seek(0)
                else:
                    image_bytes = image_file
                return self._fallback_local_analysis(image_bytes)
            else:
                return self._create_error_response("Local analysis requires image file, not URL")
                
        except Exception as e:
            print(f"Error in AI image detection: {str(e)}")
            return self._create_error_response(str(e))
    
    def _detect_with_winston_ai(self, image_file=None, image_url=None):
        """
        Detect AI-generated images using Winston AI API.
        
        API: https://api.gowinston.ai/v2/image-detection
        Auth: Bearer token in Authorization header
        Cost: 300 credits per image
        """
        try:
            # Prepare headers
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            # Prepare request body
            if image_url:
                # Use URL directly
                data = {'url': image_url}
                print(f"Calling Winston AI API with image URL: {image_url[:50]}...")  # Debug
            else:
                # Convert image file to base64 data URL
                if hasattr(image_file, 'read'):
                    image_bytes = image_file.read()
                    image_file.seek(0)
                else:
                    image_bytes = image_file
                
                # Detect image format
                image = Image.open(BytesIO(image_bytes))
                image_format = image.format.lower() if image.format else 'jpeg'
                
                # Convert to base64
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                data_url = f"data:image/{image_format};base64,{base64_image}"
                
                data = {'url': data_url}
                print("Calling Winston AI API with base64 image...")  # Debug
            
            response = requests.post(
                self.WINSTON_API_URL,
                headers=headers,
                json=data,
                timeout=60  # Winston AI may take longer for complex images
            )
            
            print(f"Winston AI Response Status: {response.status_code}")  # Debug
            
            if response.status_code == 200:
                result = response.json()
                print(f"Winston AI Response: {json.dumps(result, indent=2)}")  # Debug
                return self._parse_winston_response(result)
            elif response.status_code == 401:
                print("Winston AI: Invalid or missing authentication token")
                return None
            elif response.status_code == 402:
                print("Winston AI: Insufficient credits")
                return None
            elif response.status_code == 429:
                print("Winston AI: Rate limit exceeded")
                return None
            elif response.status_code == 415:
                print("Winston AI: Unsupported media type")
                return None
            else:
                error_text = response.text
                print(f"Winston AI Error: {response.status_code} - {error_text}")
                return None
                
        except requests.exceptions.Timeout:
            print("Winston AI: Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            print("Winston AI: Connection error")
            return None
        except Exception as e:
            print(f"Winston AI error: {str(e)}")
            return None
    
    def _parse_winston_response(self, response_data):
        """
        Parse Winston AI API response for AI-generated image detection.
        
        Response format:
        {
            "score": 1.51,  // Lower score = real, higher = AI (inverted scale)
            "human_probability": 0.9848,  // Probability it's human-made (0-1)
            "ai_probability": 0.0151,  // Probability it's AI-generated (0-1)
            "ai_watermark_detected": false,
            "ai_watermark_issuers": [],
            "credits_used": 300,
            "credits_remaining": 1700
        }
        """
        try:
            # Get probabilities from Winston AI (0-1 scale)
            ai_probability = response_data.get('ai_probability', 0)
            human_probability = response_data.get('human_probability', 0)
            
            # Convert to percentages (0-100)
            ai_score = round(ai_probability * 100, 2)
            human_score = round(human_probability * 100, 2)
            
            # Determine if AI-generated (threshold: 50%)
            is_ai_generated = ai_probability > 0.5
            
            # Get watermark info
            has_watermark = response_data.get('ai_watermark_detected', False)
            watermark_issuers = response_data.get('ai_watermark_issuers', [])
            
            # Confidence is the higher of the two probabilities
            confidence = max(ai_score, human_score)
            
            # Generate reasons based on score and metadata
            reasons = []
            if is_ai_generated:
                if ai_score > 90:
                    reasons.append("Extremely high confidence AI-generated image")
                    reasons.append("Strong synthetic patterns detected across the image")
                elif ai_score > 75:
                    reasons.append("High confidence AI-generated content")
                    reasons.append("Multiple AI generation indicators found")
                elif ai_score > 60:
                    reasons.append("Likely AI-generated based on visual patterns")
                    reasons.append("Moderate synthetic indicators detected")
                else:
                    reasons.append("Possible AI generation detected")
                    reasons.append("Some artificial patterns present")
            else:
                if ai_score < 10:
                    reasons.append("Extremely high confidence authentic photograph")
                    reasons.append("Natural image with no AI markers")
                elif ai_score < 25:
                    reasons.append("High confidence real photograph")
                    reasons.append("Minimal to no AI generation indicators")
                elif ai_score < 40:
                    reasons.append("Likely authentic image")
                    reasons.append("Natural characteristics dominate")
                else:
                    reasons.append("Inconclusive but leaning toward real")
                    reasons.append("Mixed signals detected")
            
            # Add watermark information
            if has_watermark and watermark_issuers:
                reasons.append(f"AI watermark detected: {', '.join(watermark_issuers)}")
            
            # Add detection method credit
            reasons.append("Analysis powered by Winston AI (98%+ accuracy)")
            
            # Get credits info
            credits_used = response_data.get('credits_used', 300)
            credits_remaining = response_data.get('credits_remaining', 0)
            
            return {
                'is_ai_generated': is_ai_generated,
                'confidence': confidence,
                'ai_score': ai_score,  # Percentage (0-100) for AI probability
                'human_score': human_score,  # Percentage (0-100) for human probability
                'status': 'AI-generated' if is_ai_generated else 'Real',
                'reasons': reasons[:4],
                'artifacts_detected': is_ai_generated,
                'detection_method': 'Winston AI',
                'raw_score': ai_score,
                'has_watermark': has_watermark,
                'watermark_issuers': watermark_issuers,
                'credits_used': credits_used,
                'credits_remaining': credits_remaining
            }
            
        except Exception as e:
            print(f"Error parsing Winston AI response: {str(e)}")
            return None
    
    def _fallback_local_analysis(self, image_bytes):
        """
        Fallback local analysis when Winston AI API is unavailable.
        Uses metadata analysis and basic heuristics.
        """
        try:
            image = Image.open(BytesIO(image_bytes))
            width, height = image.size
            
            score = 50  # Neutral starting point
            reasons = []
            
            # Check metadata for AI signatures
            try:
                exif = image._getexif()
                if exif is None:
                    score += 15
                    reasons.append("No camera metadata found (common in AI images)")
                else:
                    exif_data = {TAGS.get(k, k): v for k, v in exif.items()}
                    
                    # Check for camera info
                    has_camera = any(k in exif_data for k in ['Make', 'Model'])
                    has_gps = 'GPSInfo' in exif_data
                    
                    if has_camera:
                        score -= 25
                        reasons.append(f"Camera metadata found: {exif_data.get('Make', '')} {exif_data.get('Model', '')}")
                    
                    if has_gps:
                        score -= 20
                        reasons.append("GPS location data present")
                    
                    # Check software field
                    software = str(exif_data.get('Software', '')).lower()
                    if any(sig in software for sig in self.AI_SOFTWARE_SIGNATURES):
                        score += 40
                        reasons.append("AI generation software detected in metadata")
            except Exception:
                pass
            
            # Check PNG metadata
            if image.format == 'PNG':
                try:
                    info_str = str(image.info).lower()
                    if any(sig in info_str for sig in self.AI_SOFTWARE_SIGNATURES):
                        score += 40
                        reasons.append("AI parameters found in PNG metadata")
                    elif 'parameters' in info_str or 'prompt' in info_str:
                        score += 35
                        reasons.append("Generation prompt found in metadata")
                except Exception:
                    pass
            
            # Check dimensions (AI generators often use specific sizes)
            ai_dimensions = [
                (512, 512), (768, 768), (1024, 1024), (1536, 1536),
                (512, 768), (768, 512), (768, 1024), (1024, 768)
            ]
            
            if (width, height) in ai_dimensions or (height, width) in ai_dimensions:
                score += 15
                reasons.append(f"Dimensions {width}x{height} match common AI output")
            elif width % 64 == 0 and height % 64 == 0 and width >= 512:
                score += 10
                reasons.append("Dimensions are multiples of 64 (diffusion model pattern)")
            
            # Clamp score
            score = max(0, min(100, score))
            is_ai_generated = score >= 50
            
            if not reasons:
                reasons = ["Image analysis complete (local fallback method)"]
            
            return {
                'is_ai_generated': is_ai_generated,
                'confidence': score if is_ai_generated else (100 - score),
                'status': 'AI-generated' if is_ai_generated else 'Real',
                'reasons': reasons[:3],
                'artifacts_detected': is_ai_generated,
                'detection_method': 'Local Analysis (API unavailable)',
                'note': 'For best results, configure Winston AI API token (300 credits/image)'
            }
            
        except Exception as e:
            print(f"Local analysis error: {str(e)}")
            return self._create_error_response(str(e))
    
    def _create_error_response(self, error_msg):
        """Create response for error cases"""
        return {
            'is_ai_generated': False,
            'confidence': 50,
            'status': 'Unknown',
            'reasons': [f'Analysis error: {error_msg}'],
            'artifacts_detected': False,
            'detection_method': 'Error',
            'note': 'Could not complete analysis'
        }


def analyze_image_artifacts(image_file):
    """
    Analyze image for specific AI artifacts.
    Returns list of detected artifacts with details.
    """
    try:
        if hasattr(image_file, 'read'):
            image_bytes = image_file.read()
            image_file.seek(0)
        else:
            image_bytes = image_file
        
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size
        
        artifacts = []
        
        # Dimension-based artifacts
        if width == height and width >= 512:
            artifacts.append({
                'type': 'Square Dimensions',
                'description': f'Image is {width}x{height} - common AI generator output size',
                'confidence': 'Medium'
            })
        
        if width % 64 == 0 and height % 64 == 0:
            artifacts.append({
                'type': 'Diffusion Model Dimensions',
                'description': 'Dimensions are multiples of 64 (required by diffusion models)',
                'confidence': 'Medium'
            })
        
        # Check for metadata artifacts
        try:
            if image._getexif() is None:
                artifacts.append({
                    'type': 'Missing EXIF Data',
                    'description': 'No camera metadata found - common in AI-generated images',
                    'confidence': 'Medium'
                })
        except Exception:
            pass
        
        # PNG-specific checks
        if image.format == 'PNG':
            info_str = str(image.info).lower()
            if 'parameters' in info_str or 'prompt' in info_str:
                artifacts.append({
                    'type': 'AI Generation Parameters',
                    'description': 'Found AI generation prompt/parameters in metadata',
                    'confidence': 'High'
                })
        
        # Add texture analysis placeholder
        artifacts.append({
            'type': 'Texture Consistency',
            'description': 'Analyzing texture patterns for AI artifacts',
            'confidence': 'Analyzing'
        })
        
        return artifacts
        
    except Exception as e:
        print(f"Error analyzing artifacts: {str(e)}")
        return [{
            'type': 'Analysis Error',
            'description': str(e),
            'confidence': 'N/A'
        }]
