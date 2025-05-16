## 📌 Motivation

Many AI-powered image enhancement sites limit users with credit systems or paid subscriptions, making it difficult to freely upscale images. I built Upscaile to solve this — a free, intuitive platform that uses AI to upscale and enhance your images up to 4× their original resolution.

What started as a simple upload form and button gradually evolved into a full-featured web app. I experimented with frontend frameworks, APIs, and design iterations to optimize performance and usability. Today, Upscaile integrates Prodia’s AI API for enhancement, giving users a seamless and accessible experience.

tl;dr: Tired of paywalls and clunky tools for AI image upscaling? Upscaile lets you freely enhance images 4× their resolution — fast, clean, and free.

## ⚙️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python), Redis (upscale count)
- **APIs/Services**:
   - Prodia — AI upscaling (ESRGAN, SwinIR)
   - Cloudinary — Image upload/storage
   - SightEngine — Image moderation
   - Render — Web app deployment

## 🔄 How It Works
1. User uploads an image via the web interface.
2. Image is sent to Cloudinary to generate an accessible URL.
3. The Prodia API processes the image using AI upscaling models (e.g., ESRGAN, SwinIR).
4. The enhanced image URL is parsed from the Prodia response and shown to the user.
5. The original uploaded image is immediately deleted from Cloudinary for privacy.

All of this happens in just 5–10 seconds.

## 🚀 How to Use
1. Upload your image (drag & drop or file select).
- (Optional) Check the “Enhance Face” box if the image contains faces.
2. Click Submit.
3. Wait a few seconds — your upscaled image will be displayed with a shareable link.

## 🛡 License
This project follows the Creative ML OpenRAIL-M License, as specified in Prodia’s Terms of Service.

Try it out yourself at https://upscaile.onrender.com!