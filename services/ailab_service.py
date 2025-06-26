import requests
from config import Config

class AILabService:
    def __init__(self):
        self.api_key = Config.AILAB_API_KEY
        self.api_url = Config.AILAB_API_URL
        
        if not self.api_key:
            raise ValueError("AILabTools API key is required. Please set 'ailab_api_key' in your environment variables.")
    
    def upscale_image(self, image_url, upscale_factor=2, mode="base", output_format="png", output_quality=95):
        """
        Upscale image using AILabTools API
        
        Args:
            image_url (str): URL of the image to upscale
            upscale_factor (int): Magnification factor (2, 3, or 4)
            mode (str): Output mode - "base" for normal, "enhancement" for enhanced
            output_format (str): Output format - "png", "jpg", or "bmp"
            output_quality (int): Quality factor for JPG output (30-100)
            
        Returns:
            str: URL of the upscaled image, or None if failed
        """
        headers = {
            "ailabapi-api-key": self.api_key
        }
        
        # Download the image from the URL
        try:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to download image from {image_url}: {e}")
            return None
        
        # Prepare the multipart form data
        files = {
            'image': ('image.jpg', image_response.content, 'image/jpeg')
        }
        
        data = {
            'upscale_factor': upscale_factor,
            'mode': mode,
            'output_format': output_format,
            'output_quality': output_quality
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files,
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Check for API errors
            if result.get('error_code', 0) != 0:
                print(f"AILabTools API error: {result.get('error_msg', 'Unknown error')}")
                return None
            
            # Return the upscaled image URL
            return result.get('data', {}).get('url')
            
        except requests.RequestException as e:
            print(f"Failed to upscale image: {e}")
            return None
        except ValueError as e:
            print(f"Invalid JSON response: {e}")
            return None
    
    def upscale_with_face_enhancement(self, image_url, upscale_factor=2):
        """
        Upscale image with face enhancement mode
        
        Args:
            image_url (str): URL of the image to upscale
            upscale_factor (int): Magnification factor
            
        Returns:
            str: URL of the upscaled image, or None if failed
        """
        return self.upscale_image(
            image_url=image_url,
            upscale_factor=upscale_factor,
            mode="enhancement",
            output_format="png"
        ) 