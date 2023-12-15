import base64
import io
import uuid
import requests
from flask import Flask, request, render_template, flash, send_file, redirect, url_for, jsonify, Markup
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pathlib import Path
import cloudinary
import cloudinary.api
import cloudinary.uploader
#import tensorflow as tf
import json
import numpy as np
#from realesrgan_ncnn_py import Realesrgan
import cv2
from RealESRGAN import RealESRGAN
import torch

cloudinary.config(
    cloud_name = "djtemki0b",
    api_key = "149873511639713",
    api_secret = "hatlAML3ExewMgJ9GHK6HMvLxGc",
    secure=True,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.secret_key = "jskjf fkjaskj"

#app.config["MAX_CONTENT_LENGTH"] = 1000 * 1000

#realesrgan = Realesrgan(0, False, 0, 4)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RealESRGAN(device, scale=4)
model.load_weights('https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth', download=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(img_file, filename):
    # Cloudinary image upload mechanism, obtaining an image url (in order to avoid locally saved images)
    #with Image.open(img_file) as image:
       # image = realesrgan.process_pil(image)
        #image.save(f"{filename}_enhanced.jpg", quality=95)
    
    image = Image.open(img_file).convert('RGB')

    sr_image = model.predict(image)

    with io.BytesIO() as buf:
        rgb_img = sr_image.convert("RGB")
        rgb_img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()

    raw_uuid = str(uuid.uuid4())
    pub_id = ''.join(c for c in raw_uuid if c.isalnum())

    upl_resp = cloudinary.uploader.upload(image_bytes, public_id=pub_id)
    image_url = upl_resp['url']
    print(image_url, type(image_url))

    return image_url
    '''payload = json.dumps({
        "key": "nk9PYPOymevvGmoidCRWMRdtNOLoz5D67O8bHnMBkDVElp4TNB5wxXmb57VP",
        "url": image_url,
        "scale": 3,
        "webhook": None,
        "face_enhance": False
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    ----------------
    url = "https://api.getimg.ai/v1/enhancements/upscale"

    b64_str = base64.b64encode(img_bytes).decode('ascii')
    
    payload = {
        "scale": 4,
        "image": b64_str,
        "model": "real-esrgan-4x",
        "output_format": "jpeg"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer key-2j8Ul8MQ4Ktjs4ptEnAVTYh2QBM25yfseErmt5vzSU5KUFbrapTzYBLTjP2uAyDOxFgSosAvQ5yjB5eCjFnG0tKSeWAKe5IF"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    
    data = response.json();
    imgdata = base64.b64decode(data["image"])
    print(type(imgdata))

    upscaled_img_name = filename + "_upscaled.jpeg" 
    with open(filename, 'wb') as upscaled_img_file:
        upscaled_img_file.write(imgdata)

    
    return upscaled_img_file'''

    '''device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = RealESRGANer(scale=4, model_path="weights/RealESRGAN_x4plus.pth", device=device)

    model.load_state_dict(torch.load("weights/RealESRGAN_x4plus.pth"))
    model.eval()
    
#    path_to_image = 'inputs/lr_image.png'
    image = img_file.convert('RGB')

    sr_image = model(image)
    
    return sr_image'''



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    #operation = request.form.get("operation")
    if request.method == "POST":
        if "file" not in request.files:
            flash("Please select or drag and drop an image file", 'error')
            return redirect(request.url)
        file = request.files["file"]


        if file.filename == "":
            flash("Please select or drag and drop an image file", 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            blob = file.read()
            
            if int(len(blob)/(1024*1024)) > 1:
                flash("Image exceeded file size limit of 1 MB", "error")
                return redirect(request.url)
        
            filename = secure_filename(file.filename)
            
            processed_img = process_image(file, Path(file.filename).stem)
            
            #print(type(image_obj), end='a')
            #upscaled_img = upscale_image(processed_img, str(file.filename))

            flash(Markup(f"Your image has been processed and is available <a href='{processed_img}' target='_blank'>here</a>"), "success")
            
            #return render_template("index.html", upscaled_img = processed_img)
            return redirect(url_for("home"))
        
    return render_template("index.html")

app.run(debug = True)