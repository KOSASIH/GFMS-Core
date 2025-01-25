import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core Machine Learning Service API", version="1.0.0")

# Load machine learning models (replace with your model paths)
MODEL_PATHS = {
    "model1": os.getenv("MODEL1_PATH", "path/to/your/model1.joblib"),
    "model2": os.getenv("MODEL2_PATH", "path/to/your/model2.joblib"),
}

# Load models into a dictionary
models = {}
for model_name, model_path in MODEL_PATHS.items():
    try:
        models[model_name] = joblib.load(model_path)
        logger.info(f"{model_name} loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading {model_name}: {str(e)}")
        raise Exception(f"Failed to load model: {model_name}")

# Data model for input data
class PredictionInput(BaseModel):
    model_name: str
    features: list

# Endpoint to get predictions from a specified model
@app.post("/ml/predict", response_model=dict, tags=["Machine Learning"])
async def get_prediction(input_data: PredictionInput):
    """Get predictions from a specified machine learning model based on input features."""
    model_name = input_data.model_name
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Convert input features to a numpy array
        features_array = np.array(input_data.features).reshape(1, -1)
        
        # Make a prediction using the specified model
        prediction = models[model_name].predict(features_array)
        
        logger.info(f"Prediction made with {model_name}: {prediction}")
        return {"model": model_name, "prediction": prediction.tolist()}
    except Exception as e:
        logger.error(f"Error making prediction with {model_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to make prediction")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
