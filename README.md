# SEPTA Geomapping API - FastAPI

### Prerequisites
  - Python 3.10+
  - Docker
  - Docker Compose

### Getting Started
1. Clone the Repository:
```bash
git clone https://github.com/your-username/SEPTA-geomappingAPI-FastAPI.git
cd SEPTA-geomappingAPI-FastAPI
```

2. Activate the virtual environment:
```bash
source venv/bin/activate 
pip install -r requirements.txt
```

3. Make `.env` file in your root directory and copy the environment variables (bad practice to expose keys like this but this is just a test):
```bash
cp .env.example .env
```

4. Build and Start the App

Normally, in localhost, run:
```bash
uvicorn main:app --reload
```

Using DOCKER:
```bash
docker-compose up --build
```
This will build the images and start the containers.

To stop the app running in Docker:
```bash
docker-compose down
```

### API Access

- Backend is hosted at: http://localhost:8000
- Endpoints:
```bash
http://127.0.0.1:8000/                     # Root
http://127.0.0.1:8000/nearest_station/     # Nearest SEPTA station
```

To test the nearest SEPTA Station with lat and long, run:
```bash
curl -H "x-api-key: api-key-from-env" "http://127.0.0.1:8000/nearest_station?lat=39.9526&lon=-75.1652"
```

### Running Tests

To run all unit tests:
```bash
PYTHONPATH=.:$PYTHONPATH pytest tests/ -s
```

Likewise, for individual endpoint:
```bash
PYTHONPATH=.:$PYTHONPATH pytest tests/test_api.py::test_nearest_station -s
```
