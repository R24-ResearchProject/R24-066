from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import io
import numpy as np
import tensorflow as tf
import os

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = "./uploads"
CLOTHES_DIR = "./cloths"

Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)

# Load model
def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model


def check_surface(model, image):
    # Open the image and preprocess it
    img = Image.open(image)
    img = img.resize((48, 48))  # Resize the image to match model input size
    img = np.array(img)  # Convert image to numpy array
    img = img / 255.0  # Normalize pixel values
    
    # Make prediction
    prediction = model.predict(np.expand_dims(img, axis=0))
    predicted_class_index = np.argmax(prediction)
    class_names = ["Machine Surface", "Cloth surface"]
    predicted_class = class_names[predicted_class_index]
    
    return predicted_class


@app.post("/predict-cloth")
async def upload_image2(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"{UPLOADS_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Load the model
        model_path = 'model_cloth.h5'
        model = load_model(model_path)

        # Make prediction
        predicted_class = check_surface(model, file_path)

        #save to the cloths folder clothes
        if predicted_class == "Cloth surface":
            # Save the image to cloth_surface_images folder
            cloth_surface_image_path = os.path.join(CLOTHES_DIR, file.filename)
            os.rename(file_path, cloth_surface_image_path)
            return {"predicted_class": predicted_class, "image_saved": True}
        
        return {"predicted_class": predicted_class}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8000")
