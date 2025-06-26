import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='.github/envvars.env')

class Config:
    # Flask settings
    SECRET_KEY = "jjkjkl ssdnobi"
    
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.getenv("cloud_name")
    CLOUDINARY_API_KEY = os.getenv("cloudinary_key")
    CLOUDINARY_API_SECRET = os.getenv("cloudinary_secret")
    
    # Redis settings
    REDIS_URL = "https://usw2-keen-grizzly-32109.upstash.io"
    REDIS_TOKEN = os.getenv("redis_rest_token")
    
    # AILabTools API settings
    AILAB_API_KEY = os.getenv("ailab_api_key")
    AILAB_API_URL = "https://www.ailabapi.com/api/image/enhance/image-lossless-enlargement"
    
    # Sightengine settings (for moderation)
    SIGHTENGINE_WORKFLOW = os.getenv('sighteng_wid')
    SIGHTENGINE_USER = os.getenv('sighteng_user')
    SIGHTENGINE_SECRET = os.getenv('sighteng_sec')
    
    # File upload settings
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_FILE_SIZE_MB = 1
    
    # Image processing settings
    DEFAULT_UPSCALE_FACTOR = 2
    DEFAULT_OUTPUT_FORMAT = "png"
    DEFAULT_OUTPUT_QUALITY = 95 