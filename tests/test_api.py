from fastapi.testclient import TestClient
from main import app 

import os
from dotenv import load_dotenv
load_dotenv()

AUTH_API_KEY = os.getenv("AUTH_API_KEY")

client = TestClient(app)  

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the SEPTA API!"}

def test_nearest_station():
    # Specifying latitude and longitude values to test
    lat = 39.9526
    lon = -75.1652

    # Testing for the nearest septa station. Should return 200 on success.
    response = client.get(
        f"/nearest_station?lat={lat}&lon={lon}",
        headers={"x-api-key": f"Bearer {AUTH_API_KEY}"}
    )
    
    assert response.status_code == 200
    json_response = response.json()

    assert "cached" in json_response   # This should return False for first hit and True for cached data 
    assert "data" in json_response     # This should return the actual data

    # To check for more specific values/structure of the api, like for example, checking if 'features' key exists in 'data'
    assert "features" in json_response["data"]
