from fastapi import FastAPI, Depends, HTTPException, Header, Query
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

AUTH_API_KEY = os.getenv("AUTH_API_KEY")

# 7. The first and foremost solution to project API from unauthenticated users. API can only be accessed by users with a valid API_KEY. Rest return 401 unauthorized.
def api_verification(x_api_key: Optional[str] = Header(None)):

    if x_api_key != AUTH_API_KEY:
        raise HTTPException(status_code=401, detail="User Unauthorized!")
