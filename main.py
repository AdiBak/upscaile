from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from markupsafe import Markup
from services.redis_service import RedisService
from services.image_processor import ImageProcessor
from utils.file_utils import allowed_file, validate_file_size, secure_filename_safe
from config import Config
import requests
import os
import gc
import time

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Increase timeout settings
app.config['PERMANENT_SESSION_LIFETIME'] = 300  # 5 minutes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Demo images for initial preview
DEMO_ORIGINAL = "https://consolidatedlabel.com/app/uploads/2007/10/low-res-72dpi.jpg"
DEMO_ENHANCED = "https://i.ibb.co/PM8ZNX3/camelhigh.png"

# Initialize services
redis_service = RedisService()
image_processor = ImageProcessor()

def get_preview_images():
    return DEMO_ORIGINAL, DEMO_ENHANCED

def cleanup_temp_files():
    """Clean up temporary files to free memory"""
    try:
        temp_path = os.path.join("static", "uploaded_preview.jpg")
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception as e:
        print(f"Error cleaning up temp files: {e}")

@app.route("/", methods=["GET"])
def home():
    upscales_count = 0
    try:
        upscales_count = redis_service.get_upscales_count()
    except Exception as e:
        print(f"Failed to get upscales count: {e}")
    # Show demo images by default
    orig_img, enh_img = get_preview_images()
    return render_template(
        "index.html",
        upscalesCount=upscales_count,
        orig_img=orig_img,
        enh_img=enh_img,
        show_download=False
    )

@app.route("/edit", methods=["GET", "POST"])
def edit():
    upscales_count = 0
    try:
        upscales_count = redis_service.get_upscales_count()
    except Exception as e:
        print(f"Failed to get upscales count: {e}")
    orig_img, enh_img = get_preview_images()
    show_download = False
    
    if request.method == "POST":
        start_time = time.time()
        
        try:
            if "file" not in request.files:
                flash("Please select or drag and drop an image file", 'error')
                return redirect(request.url)
            
            file = request.files["file"]
            if not file or file.filename == "":
                flash("Please select or drag and drop an image file", 'error')
                return redirect(request.url)
            
            if not allowed_file(file.filename):
                flash("Image uploaded is of incompatible file type", "error")
                return redirect(url_for("home"))
            
            file_content = file.read()
            if not validate_file_size(file_content):
                flash(f"Image exceeded file size limit of {Config.MAX_FILE_SIZE_MB} MB", "error")
                return redirect(request.url)
            
            file.seek(0)
            enhance_face = request.form.get("faceEnhance") == "on"
            upscale_factor = int(request.form.get("upscale_factor", Config.DEFAULT_UPSCALE_FACTOR))
            
            # Process image with timeout handling
            processed_img_url = image_processor.process_image(
                file, 
                enhance_face=enhance_face, 
                upscale_factor=upscale_factor
            )
            
            if processed_img_url:
                flash("Success! Your image has been upscaled.", "success")
                try:
                    redis_service.increment_upscales_count()
                except Exception as e:
                    print(f"Failed to increment upscales count: {e}")
                
                # Show the user's original and enhanced images
                file.seek(0)
                # Save the uploaded file to a temp location for preview
                temp_path = os.path.join("static", "uploaded_preview.jpg")
                file.save(temp_path)
                orig_img = url_for('static', filename='uploaded_preview.jpg')
                enh_img = processed_img_url
                show_download = True
            else:
                flash("Failed to process image. Please try again.", "error")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            flash("An error occurred while processing your image. Please try again.", "error")
        finally:
            # Clean up memory
            # cleanup_temp_files()
            gc.collect()
            
            # Log processing time
            processing_time = time.time() - start_time
            print(f"Image processing completed in {processing_time:.2f} seconds")
        
        return render_template(
            "index.html",
            upscalesCount=redis_service.get_upscales_count(),
            orig_img=orig_img,
            enh_img=enh_img,
            show_download=show_download
        )
    
    # GET fallback
    return render_template(
        "index.html",
        upscalesCount=upscales_count,
        orig_img=orig_img,
        enh_img=enh_img,
        show_download=show_download
    )

# if __name__ == "__main__":
#     app.run(debug=True, host="127.0.0.1", port=5000) 