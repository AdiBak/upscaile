#!/usr/bin/env python3
"""
Setup script for Upscaile - AI Image Upscaler
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a template .env file if it doesn't exist"""
    env_path = Path('.github/envvars.env')
    
    if env_path.exists():
        print("✅ Environment file already exists at .github/envvars.env")
        return
    
    # Create directory if it doesn't exist
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create template env file
    template = """# Cloudinary Configuration
cloud_name=your_cloudinary_cloud_name
cloudinary_key=your_cloudinary_api_key
cloudinary_secret=your_cloudinary_api_secret

# AILabTools API (Required)
ailab_api_key=your_ailabtools_api_key

# Redis Configuration
redis_rest_token=your_redis_token

# Sightengine (Optional - for content moderation)
sighteng_wid=your_sightengine_workflow_id
sighteng_user=your_sightengine_user
sighteng_sec=your_sightengine_secret
"""
    
    with open(env_path, 'w') as f:
        f.write(template)
    
    print("✅ Created environment template at .github/envvars.env")
    print("📝 Please edit this file with your actual API keys and credentials")

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'pillow',
        'requests',
        'cloudinary',
        'python-dotenv',
        'upstash-redis'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up Upscaile - AI Image Upscaler")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .github/envvars.env with your API keys")
    print("2. Get your AILabTools API key from https://www.ailabtools.com/")
    print("3. Run: python test_integration.py (to test the integration)")
    print("4. Run: python app.py (to start the application)")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 