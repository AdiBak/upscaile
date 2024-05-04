import base64
import io
import uuid
import requests
import json
import yaml
from flask import Flask, request, render_template, flash, send_file, redirect, url_for, jsonify, Markup
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pathlib import Path
import cloudinary
import cloudinary.api
import cloudinary.uploader
import subprocess
from dotenv import load_dotenv

'''with open(".github/auth.yaml", 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

json.dumps(config, indent=2, sort_keys=True)

os.environ["cloud_name"] = str(config["cloudinary"]["cloud_name"])
os.environ["cloudinary_key"] = str(config["cloudinary"]["api_key"])
os.environ["cloudinary_secret"] = str(config["cloudinary"]["api_secret"])
os.environ["moderate_content_key"] = str(config["moderation"]["mod_content_key"])
os.environ["X_Prodia_Key"] = str(config["prodia"]["prodia_key"])'''

load_dotenv(dotenv_path='.github/envvars.env')

cloudinary.config(
    cloud_name = os.environ["cloud_name"], # config["cloudinary"]["cloud_name"]
    api_key = os.environ["cloudinary_key"], # config["cloudinary"]["cloudinary_key"]
    api_secret = os.environ["cloudinary_secret"], # config["cloudinary"]["cloudinary_secret"]
    secure=True,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.secret_key = "jjkjkl ssdnobi"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def image_appropriate(image_url):
    url = "https://api.moderatecontent.com/moderate/?"
    querystring = {
        "url": image_url,
        "key": os.environ["moderate_content_key"] # config["moderation"]["mod_content_key"]
    }

    response = requests.get(url, data="",headers={},params=querystring)
    data = response.json()

    if data["rating_label"] == "everyone" or data["rating_label"] == "teen":
        return True
    elif data["rating_label"] == "adult":
        return False
    
    return False

def upload_to_cloudinary_and_get_id_url(img_file):
    with io.BytesIO() as buf:
        rgb_img = Image.open(img_file).convert('RGB')
        rgb_img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()

    raw_uuid = str(uuid.uuid4())
    pub_id = ''.join(c for c in raw_uuid if c.isalnum())

    upl_resp = cloudinary.uploader.upload(image_bytes, public_id=pub_id, type="private")
    image_url = upl_resp['url']

    return pub_id, image_url


def get_result(job_id):
    url = f"https://api.prodia.com/v1/job/{job_id}"

    headers = {
        "accept": "application/json",
        "X-Prodia-Key": os.environ["X_Prodia_Key"] # config["prodia"]["prodia_key"]
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    while data["status"] != "succeeded":
        response = requests.get(url, headers=headers)
        data = response.json()

    return data["imageUrl"]


def upscale(image_url, model):
    url_upsc = "https://api.prodia.com/v1/upscale"

    payload_upsc = {
        "resize": 4,
        "model": model,
        "imageUrl": image_url
    }

    headers_upsc = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": os.environ["X_Prodia_Key"] # config["prodia"]["prodia_key"]
    }

    response_upsc = requests.post(url_upsc, json=payload_upsc, headers=headers_upsc)
    data_upsc = response_upsc.json()
    sr_image_url = get_result(data_upsc["job"])

    return sr_image_url

def increase_upscale_count():
    url = "https://counter10.p.rapidapi.com/"


def process_image(img_file, enhance_face):

    uploaded = upload_to_cloudinary_and_get_id_url(img_file)
    image_url = uploaded[1]

    if not image_appropriate(image_url):
        public_id = [uploaded[0]]
        image_delete_result = cloudinary.api.delete_resources(public_id, resource_type="image", type="private")
        return None

    if enhance_face:
        url_FE = "https://api.prodia.com/v1/facerestore"

        payload_FE = {
            "imageUrl": image_url
        }

        headers_FE = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": os.environ["X_Prodia_Key"] # config["prodia"]["prodia_key"]
        }

        response_FE = requests.post(url_FE, json=payload_FE, headers=headers_FE)
        data_FE = response_FE.json()
        enhanced_image_url = get_result(data_FE["job"])

        sr_image_url = upscale(enhanced_image_url, "ESRGAN_4x")

    else: 
        sr_image_url = upscale(image_url, "SwinIR 4x")


    public_ids = [uploaded[0]]
    image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="private")
    return sr_image_url


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

            if processed_img:
                flash(Markup(f"<p class='success'>Your image has been processed and is available <a href='{processed_img}' target='_blank'>here</a></p>"), "success")

            else:
                flash("Image is not appropriate", "error")

            with open('numUpscales.txt', 'r') as f:
                t = f.read()
            with open('numUpscales.txt', 'w') as f:
                print(str(int(t)))
                f.write(str(int(t) + 1))

            #return render_template("index.html", upscaled_img = processed_img)
            return redirect(url_for("home"))
        
    return render_template("index.html")