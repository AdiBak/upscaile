# Upscaile - AI Image Upscaler

A Flask web application that uses AILabTools API to upscale images with AI-powered enhancement.

## Features

- **AI-Powered Upscaling**: Uses AILabTools API for high-quality image upscaling
- **Face Enhancement**: Optional face enhancement mode for portrait images
- **Multiple Upscale Factors**: Support for 2x, 3x, and 4x upscaling
- **Content Moderation**: Optional image content moderation using Sightengine
- **Cloud Storage**: Temporary image storage using Cloudinary
- **Statistics Tracking**: Redis-based tracking of processed images

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.github/envvars.env` file with the following variables:

```env
# Cloudinary Configuration
cloud_name=your_cloudinary_cloud_name
cloudinary_key=your_cloudinary_api_key
cloudinary_secret=your_cloudinary_api_secret

# AILabTools API (Required)
ailab_api_key=your_ailabtools_api_key

# Redis Configuration
redis_rest_token=your_redis_token

# Sightengine (Optional - for content moderation)
sighteng_wid=your_sightengine_workflow_id
sighteng_user=your_sightengine_user
sighteng_sec=your_sightengine_secret
```

### 3. Get AILabTools API Key

1. Visit [AILabTools](https://www.ailabtools.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your environment variables as `ailab_api_key`

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## API Integration

This application integrates with the [AILabTools Image Upscaler API](https://www.ailabtools.com/doc/ai-image/enhance/image-lossless-enlargement/api) for high-quality image upscaling.

### Supported Features

- **Upscale Factors**: 2x, 3x, 4x magnification
- **Output Formats**: PNG, JPG, BMP
- **Enhancement Modes**: 
  - Base mode: Stable super-resolution effect
  - Enhancement mode: Enhanced clarity and sharpness
- **Quality Control**: Adjustable output quality for JPG format

### Image Requirements

- **Formats**: JPEG, JPG, PNG, BMP
- **Size**: Maximum 3 MB
- **Resolution**: Between 32x32px and 1920x1080px

## Project Structure

```
upscaile/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── services/             # Service modules
│   ├── __init__.py
│   ├── ailab_service.py  # AILabTools API integration
│   ├── cloudinary_service.py  # Cloudinary operations
│   ├── image_processor.py     # Main image processing workflow
│   ├── moderation_service.py  # Content moderation
│   └── redis_service.py       # Statistics tracking
├── utils/                # Utility functions
│   ├── __init__.py
│   └── file_utils.py     # File validation and processing
├── templates/            # HTML templates
│   └── index.html
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Usage

1. Upload an image file (PNG, JPG, JPEG)
2. Choose upscale factor (2x, 3x, 4x)
3. Optionally enable face enhancement
4. Click "Upscale" to process
5. Download the upscaled image from the provided link

## Deployment

The application is configured for deployment on Vercel with the included `vercel.json` configuration.

## License

This project is open source and available under the MIT License.