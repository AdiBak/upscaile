import psutil
import gc
import os

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # Convert to MB

def log_memory_usage(stage=""):
    """Log current memory usage with optional stage label"""
    memory_mb = get_memory_usage()
    print(f"Memory usage {stage}: {memory_mb:.2f} MB")
    return memory_mb

def cleanup_memory():
    """Force garbage collection and log memory cleanup"""
    before_memory = get_memory_usage()
    gc.collect()
    after_memory = get_memory_usage()
    freed_memory = before_memory - after_memory
    print(f"Memory cleanup: freed {freed_memory:.2f} MB")
    return freed_memory

def check_memory_threshold(threshold_mb=500):
    """Check if memory usage is above threshold"""
    current_memory = get_memory_usage()
    if current_memory > threshold_mb:
        print(f"Warning: High memory usage detected: {current_memory:.2f} MB")
        cleanup_memory()
        return True
    return False 