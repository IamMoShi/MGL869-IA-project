FROM fastapi-base-image

# Set a working directory
WORKDIR /production-model

# Copy files into the container
COPY requirements.production-model.txt .
COPY app app

# Install Python dependencies without cache
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.production-model.txt


# Start the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
