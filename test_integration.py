#!/usr/bin/env python3
"""
Test script for AILabTools integration
"""

import os
from dotenv import load_dotenv
from services.ailab_service import AILabService

# Load environment variables
load_dotenv(dotenv_path='.github/envvars.env')

def test_ailab_integration():
    """Test the AILabTools service integration"""
    
    # Check if API key is configured
    api_key = os.getenv("ailab_api_key")
    if not api_key:
        print("❌ AILabTools API key not found in environment variables")
        print("Please add 'ailab_api_key' to your .github/envvars.env file")
        return False
    
    print("✅ AILabTools API key found")
    
    try:
        # Initialize the service
        ailab_service = AILabService()
        print("✅ AILabService initialized successfully")
        
        # Test with a sample image URL
        test_image_url = "https://picsum.photos/200/200"  # Random test image
        
        print(f"Testing upscale with image: {test_image_url}")
        
        # Test basic upscaling
        result = ailab_service.upscale_image(
            image_url=test_image_url,
            upscale_factor=2,
            mode="base",
            output_format="png"
        )
        
        if result:
            print(f"✅ Upscaling successful! Result URL: {result}")
            return True
        else:
            print("❌ Upscaling failed - no result URL returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AILabTools integration: {e}")
        return False

if __name__ == "__main__":
    print("Testing AILabTools Integration...")
    print("=" * 40)
    
    success = test_ailab_integration()
    
    print("=" * 40)
    if success:
        print("🎉 All tests passed! AILabTools integration is working correctly.")
    else:
        print("💥 Tests failed. Please check your configuration and try again.") 