import redis
import json
import hashlib
from contextlib import contextmanager

r = redis.Redis(host="localhost", port=6379, db=0)  ## 6379 is the default Redis port

@contextmanager
def location_lock(lat, lon, timeout=10):
    key_hash = hashlib.md5(f"{lat}:{lon}".encode()).hexdigest()
    lock = r.lock(f"location:{key_hash}", timeout=timeout)
    acquired = lock.acquire(blocking=True)
    try:
        if acquired:
            yield
        else:
            raise Exception("Could not acquire lock.")
    finally:
        if acquired:
            lock.release()


def cache_data(key: str, value: dict, ttl: int = 3600):
    # Implementing Cache Value for 1 hour(3600seconds)
    r.setex(f"cache:{key}", ttl, json.dumps(value))


def get_cached_data(key:str):
    data = r.get(f"cache:{key}")
    if data:
        return json.loads(data)
        return None