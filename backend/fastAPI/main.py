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
    topo_name: str = None
    mask_name: str = None
    user_mask_name: str = None
    iou_score: float = None


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
    # Asynchronously handles the downloading of a file.
    # Args:
    #     file_name (str): The name of the file to be downloaded.
    # Returns:
    #     FileResponse: A response object that allows the client to download the specified file.
    # Note:
    #     The file is expected to be located in the "../AutoDetectData/" directory relative to the script's location.
    #     Ensure that the file exists and the path is accessible to avoid runtime errors.
    file_path = f"../AutoDetectData/{file_name}"
    return FileResponse(file_path)


# curl -X POST "http://127.0.0.1:8088/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@C:\Data\image.jpg;type=image/jpeg"
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # This module contains the FastAPI endpoint for file upload.
    # Functions:
    #     upload_file(file: UploadFile) -> dict
    #         Handles the file upload, saves the file to the specified directory, and returns a success message with the file path.

    file_name = file.filename
    file_path = f"../AutoDetectData/{file_name}"

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        return {"message": "error", "error": f"Failed to upload the file: {e}"}

    return {"message": "success", "file_path": file_path}


# curl -X POST "http://127.0.0.1:8088/load_model/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"model_name\":\"yolo_m_batch_32\", \"model_type\": \"yolo\"}"
@app.post("/load_model/")
def load_model_api(auto_detect_model: AutoDetectModel):
    # Loads a machine learning model based on the provided AutoDetectModel configuration.
    # Args:
    #     auto_detect_model (AutoDetectModel): An object containing the model's name and type.
    # Returns:
    #     dict: A dictionary containing the status of the operation.
    #           If successful, it includes a "message" key with the value "success" and the input data.
    #           If unsuccessful, it includes a "message" key with the value "error" and an "error" key with details.
    # Raises:
    #     None: This function does not raise exceptions but returns error messages in the response dictionary.
    # Notes:
    #     - The model is loaded from a predefined path: "/AutoDetectModel/{model_name}/model.pt".
    #     - If the model file does not exist or fails to load, an error message is returned.
    #     - The loaded model is stored in a global variable `model`.
    global model

    model_name = auto_detect_model.model_name
    model_type = auto_detect_model.model_type
    model_path = Path("/AutoDetectModel") / model_name / "model.pt"
    if not model_path.exists():
        return {"message": "error", "error": f"Model not found: {model_path}"}
    # model = load_model(model_path, model_type)
    if model is None:
        return {
            "message": "error",
            "error": f"Failed to load the model: {model}",
        }

    print(f"Loaded the model {model_path}")
    return {"message": "success", "data": auto_detect_model}


# curl -X POST "http://127.0.0.1:8088/detect/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"topo_name\":\"topo.raw\"}"
@app.post("/detect/")
def auto_detect(auto_detect_data: AutoDetectData):
    return {"message": "success", "data": auto_detect_data}


# To start API when using 'python main.py' command
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)


print("FastAPI server started successfully!")
