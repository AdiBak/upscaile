import base64
import io
from tempfile import NamedTemporaryFile
import uuid
import requests
from flask import Flask, request, render_template, flash, send_file, redirect, url_for, jsonify, Markup
import urllib.request
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pathlib import Path
import cloudinary
import cloudinary.api
import cloudinary.uploader
import json
import numpy as np
import cv2
import torch
import replicate

cloudinary.config(
    cloud_name = "djtemki0b",
    api_key = "149873511639713",
    api_secret = "hatlAML3ExewMgJ9GHK6HMvLxGc",
    secure=True,
)

os.environ["REPLICATE_API_TOKEN"] = "r8_2pJMAXH7hvz3xS7kB4cMGrLhsU0XP7c10tz4F"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.secret_key = "jskjf fkjaskj"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(img_file, enhance_face):

    #image = Image.open(img_file).convert('RGB')
    with io.BytesIO() as buf:
        rgb_img = Image.open(img_file).convert('RGB')
        rgb_img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()

    raw_uuid = str(uuid.uuid4())
    pub_id = ''.join(c for c in raw_uuid if c.isalnum())

    upl_resp = cloudinary.uploader.upload(image_bytes, public_id=pub_id, type="private")
    image_url = upl_resp['url']

    if enhance_face:
        sr_image = replicate.run(
            "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
            input={"img": image_url,
                   "scale": 4,
                   "version": "v1.4"}
        )
    else: 
        
        sr_image = replicate.run(
            "cjwbw/real-esrgan:d0ee3d708c9b911f122a4ad90046c5d26a0293b99476d697f6bb7f2e251ce2d4",
            input={"image": image_url,
                   "upscale": 4}
        ) 
    
    public_ids = [pub_id]
    image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="private")
    return sr_image
    



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    #operation = request.form.get("operation")
    if request.method == "POST":
        if "file" not in request.files:
            flash(Markup("<p class='error'>Please select or drag and drop an image file</p>"), 'error')
            return redirect(request.url)
        file = request.files["file"]


        if file.filename == "":
            flash(Markup("<p class='error'>Please select or drag and drop an image file</p>"), 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            blob = file.read()
            
            if int(len(blob)/(1024*1024)) > 1:
                flash("Image exceeded file size limit of 1 MB", "error")
                return redirect(request.url)

            filename = secure_filename(file.filename)
            enhance_face = request.form.get("faceEnhance")
            print(enhance_face)

            processed_img = process_image(file, enhance_face)

            flash(Markup(f"<p class='success'>Your image has been processed and is available <a href='{processed_img}' target='_blank'>here</a></p>"), "success")
            
            #return render_template("index.html", upscaled_img = processed_img)
            return redirect(url_for("home"))
        
    return render_template("index.html")

app.run(debug = True)