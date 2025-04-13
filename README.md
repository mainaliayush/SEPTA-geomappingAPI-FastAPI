This application runs in Docker containers.

Prerequisites
  - Docker
  - Docker Compose

Getting Started
1. Clone the Repository:
 ```bash
git clone https://github.com/your-username/SEPTA-geomappingAPI-FastAPI.git
cd SEPTA-geomappingAPI-FastAPI
```


3. Make .env file in your root directory and copy the environment variables(bad practice to expose keys like this but this is just a test)
```bash
cp .env.example .env
```

3. Build and Start the App
```bash
docker-compose up --build
```

This will build the images and start the containers.

To stop the app:

```bash
docker-compose down
```

- Backend is hosted at: http://localhost:8000
- Endpoints:
```bash
http://127.0.0.1:8000/                    #Root
http://127.0.0.1:8000/nearest_station/     #Nearest septa station
```


