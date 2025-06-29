# Upscaile

## 📌 Motivation

Many AI-powered image enhancement sites limit users with credit systems or paid subscriptions, making it difficult to freely upscale images. I built Upscaile to solve this — a free, intuitive platform that uses AI to upscale and enhance your images up to 4× their original resolution.

What started as a simple upload form and button gradually evolved into a full-featured web app. I experimented with frontend frameworks, APIs, and design iterations to optimize performance and usability. Today, Upscaile integrates the Hugging Face finegrain-image-enhancer API for enhancement, giving users a seamless and accessible experience.

tl;dr: Tired of paywalls and clunky tools for AI image upscaling? Upscaile lets you freely enhance images 4× their resolution — fast, clean, and free.

## ⚙️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python), Redis (upscale count)
- **APIs/Services**:
   - Hugging Face Spaces — AI upscaling ([finegrain-image-enhancer](https://huggingface.co/spaces/finegrain/finegrain-image-enhancer))
   - Cloudinary — Image upload/storage
   - SightEngine — Image moderation
   - Render — Web app deployment

## 🔄 How It Works
1. **Upload Image**: User uploads an image via the web interface (drag & drop or file select).
2. **Choose Settings**: Select the desired upscale factor (2x, 3x, or 4x) and submit.
3. **Image Moderation**: The image is checked for safety using SightEngine.
4. **Cloudinary Upload**: The image is uploaded to Cloudinary to generate a public URL.
5. **AI Enhancement**: The Hugging Face API processes the image using advanced AI upscaling models.
6. **Result Display**: The enhanced image is shown side-by-side with the original, with a download option. The original upload is deleted from Cloudinary for privacy.

All of this happens in just a few seconds.

## 🚀 How to Use
1. Upload your image (drag & drop or file select).
2. Choose your upscale factor (2x, 3x, or 4x).
3. Click Submit.
4. Wait a few seconds — your upscaled image will be displayed with a download link.

## ✨ Features
- Modern, section-based UI with gradients and clear step-by-step flow
- Side-by-side preview of original and enhanced images
- Progress bar feedback during upscaling
- Product demo carousel and "How It Works" explainer section
- No sign-up, no paywall, no watermark

## 🛠 Development Process & Updates
- **Modularization**: Refactored backend into service modules (Cloudinary, Hugging Face, moderation, Redis, file utils) for maintainability.
- **API Migration**: Utilized Hugging Face finegrain-image-enhancer API for reliable, high-quality upscaling.
- **Frontend Overhaul**: Moved CSS to a static file, improved layout, added gradients, and made the UI responsive and visually appealing.
- **User Experience**: Added progress bar, instant preview of uploaded image, and clear feedback for errors and success.
- **Security & Privacy**: All images are moderated and deleted from Cloudinary after processing.

## 🛡 License
This project follows the MIT License, as specified in the Hugging Face Space.

Try it out yourself at https://upscaile.onrender.com!

## 🏃‍♂️ Local Development

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/AdiBak/upscaile.git
   cd upscaile
   pip install -r requirements.txt
   ```
2. Set up your environment variables in `.github/envvars.env` (see setup.py for details).
3. Run the app locally:
   ```bash
   python main.py
   ```
4. Visit [http://localhost:5000](http://localhost:5000) in your browser.