import redis
import json
from typing import Any, Optional, Dict
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.default_ttl = 3600  # 1 hour default
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set a value in cache with optional TTL."""
        try:
            serialized_value = json.dumps(value)
            ttl = ttl or self.default_ttl
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get remaining TTL for a key."""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return -1
    
    def cache_spatial_data(self, spatial_id: int, data: Dict[str, Any]) -> bool:
        """Cache spatial data with a specific key pattern."""
        key = f"spatial_data:{spatial_id}"
        return self.set(key, data, ttl=1800)  # 30 minutes
    
    def get_cached_spatial_data(self, spatial_id: int) -> Optional[Dict[str, Any]]:
        """Get cached spatial data."""
        key = f"spatial_data:{spatial_id}"
        return self.get(key)
    
    def cache_analysis_result(self, analysis_type: str, params: str, result: Dict[str, Any]) -> bool:
        """Cache analysis results."""
        key = f"analysis:{analysis_type}:{hash(params)}"
        return self.set(key, result, ttl=7200)  # 2 hours
    
    def get_cached_analysis(self, analysis_type: str, params: str) -> Optional[Dict[str, Any]]:
        """Get cached analysis result."""
        key = f"analysis:{analysis_type}:{hash(params)}"
        return self.get(key)
    
    def clear_spatial_cache(self, spatial_id: int = None) -> bool:
        """Clear spatial data cache."""
        try:
            if spatial_id:
                key = f"spatial_data:{spatial_id}"
                return self.delete(key)
            else:
                # Clear all spatial data cache
                pattern = "spatial_data:*"
                keys = self.redis_client.keys(pattern)
                if keys:
                    return bool(self.redis_client.delete(*keys))
                return True
        except Exception as e:
            logger.error(f"Error clearing spatial cache: {e}")
            return False 