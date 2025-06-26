from upstash_redis import Redis
from config import Config

class RedisService:
    def __init__(self):
        self.redis = Redis(
            url=Config.REDIS_URL, 
            token=Config.REDIS_TOKEN or ""
        )
    
    def get_upscales_count(self):
        """
        Get the total number of upscales performed
        
        Returns:
            int: Number of upscales
        """
        try:
            count = self.redis.get('numUpscales')
            return int(count) if count else 0
        except Exception as e:
            print(f"Failed to get upscales count: {e}")
            return 0
    
    def increment_upscales_count(self):
        """
        Increment the upscales counter
        
        Returns:
            int: New count after increment
        """
        try:
            return self.redis.incr('numUpscales')
        except Exception as e:
            print(f"Failed to increment upscales count: {e}")
            return 0 