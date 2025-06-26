import requests
import json
from config import Config

class ModerationService:
    def __init__(self):
        self.workflow = Config.SIGHTENGINE_WORKFLOW
        self.api_user = Config.SIGHTENGINE_USER
        self.api_secret = Config.SIGHTENGINE_SECRET
    
    def is_image_appropriate(self, image_url):
        """
        Check if image is appropriate using Sightengine API
        
        Args:
            image_url (str): URL of the image to check
            
        Returns:
            bool: True if image is appropriate, False otherwise
        """
        if not all([self.workflow, self.api_user, self.api_secret]):
            print("Sightengine credentials not configured, skipping moderation")
            return True
        
        params = {
            'url': image_url,
            'workflow': self.workflow,
            'api_user': self.api_user,
            'api_secret': self.api_secret
        }
        
        try:
            response = requests.get(
                'https://api.sightengine.com/1.0/check-workflow.json', 
                params=params
            )
            response.raise_for_status()
            
            output = response.json()
            
            if output['status'] == 'failure':
                print(f"Moderation check failed: {output}")
                return False
            
            if output['summary']['action'] == 'reject':
                print(f"Image rejected by moderation: {output['summary']['reject_reason']}")
                return False
            
            return True
            
        except requests.RequestException as e:
            print(f"Failed to check image moderation: {e}")
            return False
        except (KeyError, ValueError) as e:
            print(f"Invalid moderation response: {e}")
            return False 