from functools import wraps
import json
import redis
from datetime import datetime
from flask import request

class BlogCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.recent_blogs_key = "recent_blogs"  # Global recent uploads
        self.user_recent_reads_prefix = "user_recent_reads:"  # User-specific reads
        self.max_recent_items = 10
        
    def _get_user_reads_key(self, user_id):
        """Generate Redis key for user-specific recent reads"""
        return f"{self.user_recent_reads_prefix}{user_id}"
    
    def serialize_blog(self, blog):
        """Convert blog object to JSON string"""
        blog['cached_at'] = datetime.now().isoformat()
        return json.dumps(blog)
    
    def deserialize_blog(self, blog_json):
        """Convert JSON string back to dict"""
        return json.loads(blog_json)
    
    def add_recent_blog(self, blog):
        """Add blog to recent uploads list (global)"""
        blog_json = self.serialize_blog(blog)
        pipe = self.redis_client.pipeline()
        pipe.lpush(self.recent_blogs_key, blog_json)
        pipe.ltrim(self.recent_blogs_key, 0, self.max_recent_items - 1)
        pipe.execute()
        
    def add_recent_read(self, user_id, blog):
        """Add blog to user's recently read list"""
        if not user_id:
            return  # Skip if no user_id provided
            
        user_reads_key = self._get_user_reads_key(user_id)
        blog_json = self.serialize_blog(blog)
        
        pipe = self.redis_client.pipeline()
        # Remove if already exists (to move it to front)
        pipe.lrem(user_reads_key, 0, blog_json)
        pipe.lpush(user_reads_key, blog_json)
        pipe.ltrim(user_reads_key, 0, self.max_recent_items - 1)
        # Set expiration for user's recent reads (e.g., 30 days)
        pipe.expire(user_reads_key, 60 * 60 * 24 * 30)
        pipe.execute()
        
    def get_recent_blogs(self):
        """Get list of recently uploaded blogs (global)"""
        blogs = self.redis_client.lrange(self.recent_blogs_key, 0, -1)
        return [self.deserialize_blog(blog) for blog in blogs]
    
    def get_user_recent_reads(self, user_id):
        """Get list of recently read blogs for specific user"""
        if not user_id:
            return []
            
        user_reads_key = self._get_user_reads_key(user_id)
        blogs = self.redis_client.lrange(user_reads_key, 0, -1)
        return [self.deserialize_blog(blog) for blog in blogs]
    
    def clear_user_cache(self, user_id):
        """Clear cached data for specific user"""
        user_reads_key = self._get_user_reads_key(user_id)
        self.redis_client.delete(user_reads_key)
    
    def clear_all_cache(self):
        """Clear all cached data"""
        # Clear global recent blogs
        self.redis_client.delete(self.recent_blogs_key)
        # Clear all user-specific reads (using pattern matching)
        user_keys = self.redis_client.keys(f"{self.user_recent_reads_prefix}*")
        if user_keys:
            self.redis_client.delete(*user_keys)

cache = BlogCache()
# Create decorator for caching with user context
def cache_blog_read(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 200:
            blog_data = response.get_json()
            if blog_data and hasattr(request, 'user_id'):
                cache.add_recent_read(request.user_id, blog_data)
        return response
    return decorated_function


