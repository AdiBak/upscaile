## 📌 Motivation

Many AI-powered image enhancement sites limit users with credit systems or paid subscriptions, making it difficult to freely upscale images. I built **Upscaile** to solve this — a free, intuitive platform that uses AI to upscale and enhance your images up to 4× their original resolution.

I wanted users to experience the power of modern AI models without the friction of paywalls, account creation, or clunky interfaces.

---

## 🛠 Development Process

I started by building a simple HTML frontend — just a file input and a submit button — to experiment with file uploads and basic form handling.

From there, I explored various APIs for upscaling and hosting. After testing several options, I chose:

- **Cloudinary** to upload images and generate shareable URLs,
- **Prodia** for high-quality AI upscaling using models like ESRGAN and SwinIR,
- **SightEngine** for image moderation to ensure content safety.

Once I had a working API pipeline, I built a Flask backend to handle requests, call the APIs, and manage state (like image counts) using Redis.

On the frontend, I gradually introduced Bootstrap for styling and responsiveness, added loading spinners, flash messages, and a carousel to showcase enhanced image comparisons. Throughout, I focused on clean UX, privacy (automatic deletion of originals), and speed.

The final deployed version runs on **Render** and delivers a seamless experience — uploading, processing, and delivering upscaled results in about **5–10 seconds**.

---

## ⚙️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Backend**: Flask (Python), Redis (upscale count tracking)  
- **APIs/Services**:
  - **Prodia** — AI upscaling (ESRGAN, SwinIR)
  - **Cloudinary** — Image upload & URL generation
  - **SightEngine** — Image moderation
  - **Render** — Web app deployment

---

## 🔄 How It Works

1. User uploads an image through the web interface.
2. The image is uploaded to **Cloudinary** to generate a public URL.
3. The **Prodia API** processes the image using AI-based upscaling models (e.g., ESRGAN, SwinIR).
4. The upscaled image URL is extracted from the response and displayed to the user.
5. The original image is deleted from Cloudinary immediately to protect privacy.

⚡️ All of this happens in just **5–10 seconds**.

---

## 🚀 How to Use

1. Upload your image (drag & drop or file select).
2. *(Optional)* Check the **“Enhance Face”** box if your image contains faces.
3. Click **Submit**.
4. Wait a few seconds — your upscaled image and a shareable link will appear.

---

## 🛡 License

This project follows the **Creative ML OpenRAIL-M License**, as specified in [Prodia’s Terms of Service](https://prodia.com/terms).

---

👉 **Try it out:** [https://upscaile.onrender.com](https://upscaile.onrender.com)
