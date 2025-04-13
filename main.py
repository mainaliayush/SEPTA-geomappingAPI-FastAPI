from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from utils.calculate_haversine import *
from utils.retrieve_datasets import *
from utils.walking_directions import *
from utils.auth_api_verification import *
from redisCache.redis_cache import *
from utils.rate_limiter import init_redis_rate_limiter, rate_limit_free_hourly
from utils.request_logger import log_requests

import os
from dotenv import load_dotenv
load_dotenv()


ORS_API_KEY = os.getenv("ORS_API_KEY")

app = FastAPI()
app.middleware("http")(log_requests)

# 7. Protecting API against malicious users using CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*", "localhost"])

# Redirecting HTTP to HTTPS, for prod in future
# app.add_middleware(HTTPSRedirectMiddleware)

# Custom Security middleware to add security headers to all responses
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# FastAPI event to initialize Redis rate limiter on startup
@app.on_event("startup")
async def startup_event():
    await init_redis_rate_limiter()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the SEPTA API!"}

## 2. API that finds the nearest station on the basis of given latitude and longitude
@app.get("/nearest_station", dependencies=[Depends(api_verification), Depends(rate_limit_free_hourly)] )

async def nearest_station(lat: float, lon: float):  # 6. Turning this function asynchronous to handle million users in a non-blocking, fast and efficient manner

    # 5. Latitude and longitude validation check. Returns sensible API for anybody using from any place
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    location_key = f"{lat:.4f}_{lon:.4f}" # 5. Rounding the coordinates to 4 decimal place precision point 

    cached_data = get_cached_data(location_key)

    # 4. Checking if the requested data is already in cache. If yes, returning requests from cache without depleting API for the same request 
    if cached_data:
        return {
            "cached": True,
            "message": "Location already processed. Retrieving data from cache now",
            "data": cached_data 
        }

    # 3. Implementing Redis locking mechanism to ensure API does not search for same location more than once
    with location_lock(lat, lon):
        stations_data = get_septa_data('data/septa.kmz')

        nearest_station = None
        minimum_distance = float('inf')
        
        for station in stations_data:
            station_lat, station_lon = station['coordinates']
            distance = haversine(lat, lon, station_lat, station_lon)
            if distance < minimum_distance:
                nearest_station = station
                minimum_distance = distance

        if not nearest_station:
            raise HTTPException(status_code=404, detail="No nearby station found")

        try:
            # Awaiting get_walking_directions for async optimization 
            walking_route = await get_walking_directions(
                [lon, lat],  
                [station_lon, station_lat], 
                ors_api_key=ORS_API_KEY
            )
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to get walking directions: {str(e)}")

        # Returning the result in GeoJSON format
        result = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            nearest_station['coordinates'][1], 
                            nearest_station['coordinates'][0]   
                        ]
                    },
                    "properties": {
                        "name": nearest_station["name"],
                        "distance_km": round(minimum_distance, 3),
                        "kind": "station"
                    }
                },
                *walking_route["features"]  
            ]
        }

        # Caching the result to Redis before returning the result
        cache_data(location_key, result)

        return {
            "cached": False, 
            "data":result
        }
