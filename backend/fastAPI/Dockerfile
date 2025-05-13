FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy files into the container
COPY requirements.txt .
COPY *.py .

# Install Python dependencies without cache
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

# Start the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
