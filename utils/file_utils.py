from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """
    Check if the file extension is allowed
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_file_size(file_content, max_size_mb=None):
    """
    Validate file size
    
    Args:
        file_content (bytes): File content
        max_size_mb (int): Maximum file size in MB
        
    Returns:
        bool: True if file size is within limit, False otherwise
    """
    if max_size_mb is None:
        max_size_mb = Config.MAX_FILE_SIZE_MB
    
    file_size_mb = len(file_content) / (5 * 1024 * 1024)
    return file_size_mb <= max_size_mb

def secure_filename_safe(filename):
    """
    Safely secure filename, handling None values
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Secured filename or empty string if None
    """
    if not filename:
        return ""
    return secure_filename(filename) 