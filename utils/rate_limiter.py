from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from aioredis import from_url
import os

async def init_redis_rate_limiter():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis = from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

# 7. Rate limiting will help against malicious by timing out with a 429, saving server from potential DDoS

rate_limit_anonymous = RateLimiter(times=5, seconds=60)
rate_limit_free = RateLimiter(times=30, seconds=60)
rate_limit_free_hourly = RateLimiter(times=500, seconds=3600)
rate_limit_premium = RateLimiter(times=100, seconds=60)
