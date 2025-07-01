from gradio_client import Client, file
import base64
import mimetypes
import os
import time
from config import Config

# Default parameters for finegrain API
DEFAULT_PARAMS = {
    'prompt': 'best quality',
    'negative_prompt': 'worst quality',
    'seed': 0,
    'upscale_factor': 4,
    'controlnet_scale': 0.4,
    'controlnet_decay': 0.525,
    'condition_scale': 4,
    'tile_width': 73,
    'tile_height': 67,
    'denoise_strength': 0.1,
    'num_inference_steps': 19,
    'solver': 'DDIM',
}

# Initialize client
client = Client("finegrain/finegrain-image-enhancer")

def enhance_image(image_url, params=None):
    """
    Calls the Hugging Face finegrain-image-enhancer API with the given image URL and parameters.
    Returns the enhanced image as a data URL (base64) if a local file is returned, or a URL if available.
    """
    start_time = time.time()
    
    try:
        p = DEFAULT_PARAMS.copy()
        if params:
            p.update(params)
        
        print(f"Starting image enhancement with upscale_factor: {p['upscale_factor']}")
        
        # Set a longer timeout for the prediction call
        result = client.predict(
            file(image_url),
            p['prompt'],
            p['negative_prompt'],
            p['seed'],
            p['upscale_factor'],
            p['controlnet_scale'],
            p['controlnet_decay'],
            p['condition_scale'],
            p['tile_width'],
            p['tile_height'],
            p['denoise_strength'],
            p['num_inference_steps'],
            p['solver'],
            api_name="/process"
        )
        
        processing_time = time.time() - start_time
        print(f"Hugging Face API call completed in {processing_time:.2f} seconds")
        print("Full result:", result)
        
        # Result is a tuple (orig, enhanced)
        if result and len(result) > 1:
            enhanced_path = result[1]
            if isinstance(enhanced_path, str) and os.path.exists(enhanced_path):
                mime_type, _ = mimetypes.guess_type(enhanced_path)
                with open(enhanced_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                data_url = f"data:{mime_type};base64,{encoded}"
                
                # Clean up the temporary file
                try:
                    os.remove(enhanced_path)
                except Exception as e:
                    print(f"Warning: Could not remove temp file {enhanced_path}: {e}")
                
                return data_url
        
        print("No enhanced image found")
        return None
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"Error in Hugging Face API call after {processing_time:.2f} seconds: {e}")
        return None 