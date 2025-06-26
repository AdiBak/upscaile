from flask import Flask, request, render_template, flash, redirect, url_for
from markupsafe import Markup
from services.redis_service import RedisService
from services.image_processor import ImageProcessor
from utils.file_utils import allowed_file, validate_file_size, secure_filename_safe
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize services
redis_service = RedisService()
image_processor = ImageProcessor()

@app.route("/")
def home():
    """Home page showing the upload form and upscales count"""
    try:
        upscales_count = redis_service.get_upscales_count()
    except Exception as e:
        print(f"Failed to get upscales count: {e}")
        upscales_count = 0
    
    return render_template("index.html", upscalesCount=upscales_count)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Handle image upload and processing"""
    if request.method == "POST":
        # Check if file was uploaded
        if "file" not in request.files:
            flash("Please select or drag and drop an image file", 'error')
            return redirect(request.url)
        
        file = request.files["file"]
        
        # Check if file was selected
        if not file or file.filename == "":
            flash("Please select or drag and drop an image file", 'error')
            return redirect(request.url)
        
        # Validate file type
        if not allowed_file(file.filename):
            flash("Image uploaded is of incompatible file type", "error")
            return redirect(url_for("home"))
        
        # Validate file size
        file_content = file.read()
        if not validate_file_size(file_content):
            flash(f"Image exceeded file size limit of {Config.MAX_FILE_SIZE_MB} MB", "error")
            return redirect(request.url)
        
        # Reset file pointer for processing
        file.seek(0)
        
        # Get form parameters
        enhance_face = request.form.get("faceEnhance") == "on"
        upscale_factor = int(request.form.get("upscale_factor", Config.DEFAULT_UPSCALE_FACTOR))
        
        # Process the image
        try:
            processed_img_url = image_processor.process_image(
                file, 
                enhance_face=enhance_face, 
                upscale_factor=upscale_factor
            )
            
            if processed_img_url:
                flash(
                    Markup(f"Success! Here is the link to your <a href='{processed_img_url}' target='_blank'>upscaled image</a></p>"), 
                    "success"
                )
                
                # Increment upscales count
                try:
                    redis_service.increment_upscales_count()
                except Exception as e:
                    print(f"Failed to increment upscales count: {e}")
            else:
                flash("Failed to process image. Please try again.", "error")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            flash("An error occurred while processing your image. Please try again.", "error")
        
        return redirect(url_for("home"))
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000) 