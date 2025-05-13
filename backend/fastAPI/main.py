import os
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

# import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

app = FastAPI()

# Create a global variable model
model = None


@dataclass
class AutoDetectData:
    image_name: str = None
    

@dataclass
class AutoDetectModel:
    model_name: str = None
    model_type: str = None


# Root URL
# curl http://127.0.0.1:8088/docs
@app.get("/")
def root():
    return {"MGL869 FastAPI v0.1"}


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    """
    Handles the download of a file from the server.

    Args:
        file_name (str): The name of the file to be downloaded.

    Returns:
        FileResponse: A FastAPI FileResponse object that streams the file to the client.

    Notes:
        - The file is retrieved from the "../AutoDetectData/" directory relative to the script's location.
        - If the file does not exist, FastAPI will raise a 404 error automatically.
    """
    file_path = f"../AutoDetectData/{file_name}"
    return FileResponse(file_path)


# curl -X POST "http://127.0.0.1:8088/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@C:\Data\image.jpg;type=image/jpeg"
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles the upload of a file to the server.
    Args:
        file (UploadFile): The file to be uploaded, provided as a FastAPI UploadFile object.
    Returns:
        dict: A dictionary containing:
            - "message" (str): Status of the operation ("success" or "error").
            - "file_path" (str, optional): The path where the file was saved (only if successful).
            - "error" (str, optional): Error message in case of failure.
    Raises:
        Exception: If there is an issue while writing the file to the specified path.
    Notes:
        - The file is saved to the "../AutoDetectData/" directory relative to the script's location.
        - The function reads the file content asynchronously and writes it to the specified path.
    """
    file_name = file.filename
    file_path = f"../AutoDetectData/{file_name}"
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        return {"message": "error", "error": f"Failed to upload the file: {e}"}

    return {"message": "success", "file_path": file_path}


# curl -X POST "http://127.0.0.1:8088/detect/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"topo_name\":\"topo.raw\"}"
@app.post("/detect/")
def auto_detect(auto_detect_data: AutoDetectData):
    # This module contains the FastAPI endpoint for automatic detection.
    return {"message": "success", "data": auto_detect_data}


@app.post("/detect2/")
def detect2(file: UploadFile = File(...)):
    """
    Handles the detection process for an uploaded file.

    This function uploads the provided file, performs automatic detection
    on the uploaded file, and returns a success message along with the
    filename.

    Args:
        file (UploadFile): The file to be uploaded and processed.

    Returns:
        dict: A dictionary containing a success message and the filename of the uploaded file.
    """
    upload_file(file)
    auto_detect(AutoDetectData(image_name=file.filename))
    return {"message": "success", "file": file.filename}


# To start API when using 'python main.py' command
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)


print("FastAPI server started successfully!")
