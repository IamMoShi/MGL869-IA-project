FROM python:3.13-slim

# Set a working directory
WORKDIR /ia-api

# Copy files into the container
COPY requirements.ia-api.txt .
COPY app app

# Install Python dependencies without cache
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.ia-api.txt


# Start the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
