**Motivation**

When I tried to enhance my images using AI online, I noticed that many existing sites don't offer a seamless experience – I was equipped with a limited number of "credits" which diminish for every upscale operation, and when they hit 0, the only options were to purchase a pack of credits or a subscription. I didn't want either. The lack of intuitive and free software prompted me to develop a platform that employs AI to upsc'AI'le (hence the name lol) and enhance your images 4x their original resolution. 

Upscaile began primitively, containing only an input file form and a submit button. Gradually, I’ve experimented with different frontend designs, APIs, and libraries in an attempt to maximize usability and efficiency. I currently integrate Prodia’s AI-based enhancement API to perform upscaling, subsequently displaying the link to the new image. 

_tl;dr:_ Have you ever struggled to enhance your images due to the lack of effective and free AI-based software? I understand your frustration, which is why I have developed a platform to seamlessly upsc'AI'le and enhance your images 4x their original resolution. 

**Tech Stack**

Prodia for AI API, Cloudinary for image upload API, SightEngine for image moderation API, Render for web app deployment, Javascript/HTML/CSS/Bootstrap for frontend, Flask & Redis for backend 

First, when the user uploads an image, it it sent to Cloudinary so that an accessible URL can be generated. 
Next, the Prodia API accepts a URL to an image and upscales it using artificial intelligence algorithms like ESRGAN and SWIN-IR. 
Then, the URL to this upscaled image is fetched from the resulting JSON response and incorporated into the web page. 
Finally, to ensure data privacy, the original user-uploaded image is immediately deleted from the Cloudinary server.

As a whole, this process takes just about 5-10 seconds.

**How to Use**

First, drag and drop your image file, or select your image, in the input field.
Next, check if you want to enhance a face, or leave it unchecked otherwise.
Then, hit submit.

After a few seconds, a link to your upscaled image will be displayed on the screen. It’s that easy! 

**License**

Follows the Creative ML OpenRail -M License as stated in Prodia’s TOS.
