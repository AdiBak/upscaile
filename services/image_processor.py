from services.cloudinary_service import CloudinaryService
from services.huggingface_service import enhance_image
from services.moderation_service import ModerationService
from utils.memory_utils import log_memory_usage, cleanup_memory, check_memory_threshold
from config import Config
import time
import gc

class ImageProcessor:
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.moderation_service = ModerationService()
    
    def process_image(self, img_file, enhance_face=False, upscale_factor=2):
        """
        Process image through the complete workflow:
        1. Upload to Cloudinary
        2. Check moderation (optional)
        3. Upscale with Hugging Face API
        4. Clean up temporary files
        
        Args:
            img_file: FileStorage object from Flask
            enhance_face (bool): (ignored)
            upscale_factor (int): Upscaling factor (2, 3, or 4)
            
        Returns:
            str: URL of the upscaled image, or None if processing failed
        """
        start_time = time.time()
        public_id = None
        
        try:
            log_memory_usage("at start")
            print(f"Starting image processing with upscale_factor: {upscale_factor}")
            
            # Step 1: Upload to Cloudinary
            print("Uploading image to Cloudinary...")
            public_id, image_url = self.cloudinary_service.upload_image(img_file)
            print(f"Image uploaded to Cloudinary with public_id: {public_id}")
            log_memory_usage("after Cloudinary upload")
            
            # Check memory threshold
            check_memory_threshold()
            
            # Step 2: Check moderation (optional)
            print("Checking image moderation...")
            if not self.moderation_service.is_image_appropriate(image_url):
                print("Image failed moderation check")
                self.cloudinary_service.delete_image(public_id)
                return None
            
            log_memory_usage("after moderation check")
            
            # Step 3: Upscale with Hugging Face API
            print("Starting Hugging Face API enhancement...")
            params = {'upscale_factor': upscale_factor}
            upscaled_url = enhance_image(image_url, params)
            
            log_memory_usage("after Hugging Face API")
            
            if upscaled_url:
                print("Image enhancement completed successfully")
            else:
                print("Image enhancement failed")
            
            # Step 4: Clean up temporary files
            print("Cleaning up temporary files...")
            self.cloudinary_service.delete_image(public_id)
            
            processing_time = time.time() - start_time
            print(f"Total image processing completed in {processing_time:.2f} seconds")
            
            return upscaled_url
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Error processing image after {processing_time:.2f} seconds: {e}")
            
            # Clean up on error
            try:
                if public_id:
                    print(f"Cleaning up Cloudinary image: {public_id}")
                    self.cloudinary_service.delete_image(public_id)
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")
            
            return None
        finally:
            # Force garbage collection to free memory
            cleanup_memory()
            log_memory_usage("at end") 