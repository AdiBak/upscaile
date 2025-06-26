import io
import uuid
from PIL import Image
import cloudinary
import cloudinary.api
import cloudinary.uploader
from config import Config

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
            secure=True,
        )
    
    def upload_image(self, img_file):
        """
        Upload image to Cloudinary and return public_id and URL
        
        Args:
            img_file: FileStorage object from Flask
            
        Returns:
            tuple: (public_id, image_url)
        """
        with io.BytesIO() as buf:
            rgb_img = Image.open(img_file).convert('RGB')
            rgb_img.save(buf, 'jpeg')
            image_bytes = buf.getvalue()

        raw_uuid = str(uuid.uuid4())
        pub_id = ''.join(c for c in raw_uuid if c.isalnum())

        upl_resp = cloudinary.uploader.upload(
            image_bytes, 
            public_id=pub_id, 
            type="private"
        )
        image_url = upl_resp['url']

        return pub_id, image_url
    
    def delete_image(self, public_id):
        """
        Delete image from Cloudinary
        
        Args:
            public_id: The public ID of the image to delete
            
        Returns:
            dict: Deletion result from Cloudinary
        """
        return cloudinary.api.delete_resources(
            [public_id], 
            resource_type="image", 
            type="private"
        ) 