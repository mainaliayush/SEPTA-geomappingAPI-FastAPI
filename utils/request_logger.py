# request_logger.py
from datetime import datetime
from fastapi import Request

async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] Request from {client_ip}: {request.method} {request.url.path}")
    
    # Optionally log to file/db here
    response = await call_next(request)
    return response
