#  Official Python image
FROM python:3.10-slim

# Environment variables setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Working directory setup
WORKDIR /app

# System dependencies Installations
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pip packages installations
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Exposing port that runs the server
EXPOSE 8000

# Running the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
