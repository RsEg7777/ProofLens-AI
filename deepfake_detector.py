"""
ProofLens AI - Arya.ai Deepfake Detection Module
Handles video, image, and audio deepfake detection using Arya.ai APIs
"""

import requests
from config import Config
from typing import Dict, Any, Optional
import base64


class DeepfakeDetectorBase:
    """Base class for deepfake detection"""
    
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Make API request to Arya.ai"""
        try:
            # Convert file to base64
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            
            payload = {
                'file': encoded_file,
                'filename': filename
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=120  # 2 minutes timeout for processing
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            return {
                'error': 'Request timeout',
                'status': 'error',
                'message': 'The analysis is taking longer than expected. Please try again.'
            }
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'status': 'error',
                'message': 'Failed to communicate with detection service'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error',
                'message': 'An unexpected error occurred during analysis'
            }
    
    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and standardize API response"""
        if 'error' in response:
            return {
                'is_deepfake': False,
                'confidence': 0,
                'status': 'Error',
                'reasons': [response.get('message', 'Unknown error')],
                'raw_response': response
            }
        
        # Extract relevant fields from Arya.ai response
        # Adjust these based on actual Arya.ai API response format
        is_deepfake = response.get('is_manipulated', False)
        confidence = response.get('confidence_score', 0.0)
        
        return {
            'is_deepfake': is_deepfake,
            'confidence': round(confidence * 100, 2),  # Convert to percentage
            'status': 'Deepfake Detected' if is_deepfake else 'Authentic',
            'reasons': response.get('indicators', []),
            'manipulation_type': response.get('manipulation_type', 'Unknown'),
            'raw_response': response
        }


class VideoDeepfakeDetector(DeepfakeDetectorBase):
    """Detect deepfakes in video files"""
    
    def __init__(self, api_token: Optional[str] = None):
        api_url = Config.ARYA_VIDEO_API_URL
        api_token = api_token or Config.ARYA_VIDEO_API_TOKEN
        
        if not api_url or not api_token:
            raise ValueError("Video detection API URL and token must be configured")
        
        super().__init__(api_url, api_token)
    
    def detect_video_deepfake(self, video_file) -> Dict[str, Any]:
        """
        Detect if a video is a deepfake
        
        Args:
            video_file: File object or bytes
            
        Returns:
            Dictionary with detection results
        """
        # Read file data
        if hasattr(video_file, 'read'):
            video_file.seek(0)
            file_data = video_file.read()
            filename = getattr(video_file, 'filename', 'video.mp4')
        else:
            file_data = video_file
            filename = 'video.mp4'
        
        # Make API request
        response = self._make_request(file_data, filename)
        
        # Parse and return results
        return self._parse_response(response)


class ImageDeepfakeDetector(DeepfakeDetectorBase):
    """Detect deepfakes in image files (alternative to Winston AI)"""
    
    def __init__(self, api_token: Optional[str] = None):
        api_url = Config.ARYA_IMAGE_API_URL
        api_token = api_token or Config.ARYA_IMAGE_API_TOKEN
        
        if not api_url or not api_token:
            raise ValueError("Image detection API URL and token must be configured")
        
        super().__init__(api_url, api_token)
    
    def detect_image_deepfake(self, image_file) -> Dict[str, Any]:
        """
        Detect if an image is a deepfake
        
        Args:
            image_file: File object or bytes
            
        Returns:
            Dictionary with detection results
        """
        # Read file data
        if hasattr(image_file, 'read'):
            image_file.seek(0)
            file_data = image_file.read()
            filename = getattr(image_file, 'filename', 'image.jpg')
        else:
            file_data = image_file
            filename = 'image.jpg'
        
        # Make API request
        response = self._make_request(file_data, filename)
        
        # Parse and return results
        return self._parse_response(response)


class AudioDeepfakeDetector(DeepfakeDetectorBase):
    """Detect deepfakes in audio files"""
    
    def __init__(self, api_token: Optional[str] = None):
        api_url = Config.ARYA_AUDIO_API_URL
        api_token = api_token or Config.ARYA_AUDIO_API_TOKEN
        
        if not api_url or not api_token:
            raise ValueError("Audio detection API URL and token must be configured")
        
        super().__init__(api_url, api_token)
    
    def detect_audio_deepfake(self, audio_file) -> Dict[str, Any]:
        """
        Detect if an audio file is a deepfake
        
        Args:
            audio_file: File object or bytes
            
        Returns:
            Dictionary with detection results
        """
        # Read file data
        if hasattr(audio_file, 'read'):
            audio_file.seek(0)
            file_data = audio_file.read()
            filename = getattr(audio_file, 'filename', 'audio.mp3')
        else:
            file_data = audio_file
            filename = 'audio.mp3'
        
        # Make API request
        response = self._make_request(file_data, filename)
        
        # Parse and return results
        return self._parse_response(response)


# Convenience function for quick detection
def detect_deepfake(file, media_type: str) -> Dict[str, Any]:
    """
    Detect deepfake based on media type
    
    Args:
        file: File object or bytes
        media_type: 'video', 'image', or 'audio'
        
    Returns:
        Dictionary with detection results
    """
    try:
        if media_type == 'video':
            detector = VideoDeepfakeDetector()
            return detector.detect_video_deepfake(file)
        elif media_type == 'image':
            detector = ImageDeepfakeDetector()
            return detector.detect_image_deepfake(file)
        elif media_type == 'audio':
            detector = AudioDeepfakeDetector()
            return detector.detect_audio_deepfake(file)
        else:
            return {
                'is_deepfake': False,
                'confidence': 0,
                'status': 'Error',
                'reasons': [f'Unsupported media type: {media_type}']
            }
    except Exception as e:
        return {
            'is_deepfake': False,
            'confidence': 0,
            'status': 'Error',
            'reasons': [str(e)]
        }
