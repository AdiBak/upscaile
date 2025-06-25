## 📌 Motivation

Many AI-powered image enhancement sites limit users with credit systems or paywalls, making it frustrating to freely upscale images. I wanted to build an alternative — a simple, fast, and free solution that anyone could use without restriction.

This project also gave me an opportunity to explore AI APIs and strengthen my backend skills — especially with Flask, which I’d been meaning to learn through a real-world build.

---

## 🧱 Development Process

**Upscaile** began as a minimal prototype: just an HTML form with a file input and submit button. From there, I explored several APIs and tools to bring the concept to life.

Here’s a rough timeline of how I developed it:

1. **Flask Backend Setup**: Built a basic Flask server to handle image uploads and route requests.
2. **API Research & Integration**:
   - Tried various AI upscaling APIs and selected **Prodia** for its performance and simplicity.
   - Used **Cloudinary** for quick image uploads and public URL generation.
   - Integrated **SightEngine** for basic moderation to ensure uploaded content is appropriate.
3. **Frontend Design**:
   - Started with static HTML/CSS, then added **Bootstrap** for a clean, responsive UI.
   - Added image carousels to visually compare before and after results.
4. **Optimization & Privacy**:
   - Ensured images are deleted from Cloudinary immediately after use.
   - Added Redis to track total upscale counts.
5. **Deployment**:
   - Deployed the app using **Render**, making it publicly accessible.

Throughout the process, I focused on learning Flask, building an intuitive user experience, and keeping the pipeline fast and secure.

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
2. The image is sent to **Cloudinary** to generate a public URL.
3. The **Prodia API** upscales the image using AI models.
4. The resulting high-res image URL is extracted and shown to the user.
5. The original image is then deleted from Cloudinary to maintain privacy.

⚡️ This entire flow typically takes **5–10 seconds**.

---

## 🚀 How to Use

1. Upload your image (drag & drop or file select).
2. *(Optional)* Check the **“Enhance Face”** box if the image contains faces.
3. Click **Submit**.
4. Your upscaled image and a shareable link will appear within seconds.

---

## 🛡 License

This project follows the **Creative ML OpenRAIL-M License**, as specified in [Prodia’s Terms of Service](https://prodia.com/terms).

---

👉 **Live Demo**: [https://upscaile.onrender.com](https://upscaile.onrender.com)
