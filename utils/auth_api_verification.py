from fastapi import FastAPI, Depends, HTTPException, Header, Query
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

AUTH_API_KEY = os.getenv("AUTH_API_KEY")

def api_verification(x_api_key: Optional[str] = Header(None)):

    if x_api_key != AUTH_API_KEY:
        raise HTTPException(status_code=401, detail="User Unauthorized!")
