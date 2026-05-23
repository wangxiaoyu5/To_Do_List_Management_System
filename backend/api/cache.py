from django.core.cache import cache
from functools import wraps
import hashlib
import json


def get_cache_key(prefix: str, user_id: str = None, **kwargs) -> str:
    """生成缓存键"""
    key_parts = [prefix]
    if user_id:
        key_parts.append(str(user_id))
    
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cache_result(prefix: str, timeout: int = 300):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = get_cache_key(prefix, **kwargs)
            cached_result = cache.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


def invalidate_user_cache(user_id: str, prefix: str = None):
    """清除用户相关的缓存"""
    if prefix:
        cache.delete(get_cache_key(prefix, user_id))
    else:
        cache.delete_pattern(f"*{user_id}*")
