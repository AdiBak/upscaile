from services.cloudinary_service import CloudinaryService
from services.ailab_service import AILabService
from services.moderation_service import ModerationService

class ImageProcessor:
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.ailab_service = AILabService()
        self.moderation_service = ModerationService()
    
    def process_image(self, img_file, enhance_face=False, upscale_factor=2):
        """
        Process image through the complete workflow:
        1. Upload to Cloudinary
        2. Check moderation (optional)
        3. Upscale with AILabTools
        4. Clean up temporary files
        
        Args:
            img_file: FileStorage object from Flask
            enhance_face (bool): Whether to use face enhancement mode
            upscale_factor (int): Upscaling factor (2, 3, or 4)
            
        Returns:
            str: URL of the upscaled image, or None if processing failed
        """
        try:
            # Step 1: Upload to Cloudinary
            public_id, image_url = self.cloudinary_service.upload_image(img_file)
            
            # Step 2: Check moderation (optional)
            if not self.moderation_service.is_image_appropriate(image_url):
                print("Image failed moderation check")
                self.cloudinary_service.delete_image(public_id)
                return None
            
            # Step 3: Upscale with AILabTools
            if enhance_face:
                upscaled_url = self.ailab_service.upscale_with_face_enhancement(
                    image_url, upscale_factor
                )
            else:
                upscaled_url = self.ailab_service.upscale_image(
                    image_url, upscale_factor
                )
            
            # Step 4: Clean up temporary files
            self.cloudinary_service.delete_image(public_id)
            
            return upscaled_url
            
        except Exception as e:
            print(f"Error processing image: {e}")
            # Clean up on error
            try:
                if 'public_id' in locals():
                    self.cloudinary_service.delete_image(public_id)
            except:
                pass
            return None 