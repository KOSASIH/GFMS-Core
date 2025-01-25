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
app = FastAPI(title="GFMS-Core AI Service API", version="1.0.0")

# Load the pre-trained model (replace with your model path)
MODEL_PATH = os.getenv("MODEL_PATH", "path/to/your/model.joblib")
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise Exception("Failed to load the model.")

# Data model for input data
class PredictionInput(BaseModel):
    features: list

# Endpoint to get AI-driven insights
@app.post("/ai/predict", response_model=dict, tags=["AI Service"])
async def get_insight(input_data: PredictionInput):
    """Get AI-driven insights based on input features."""
    try:
        # Convert input features to a numpy array
        features_array = np.array(input_data.features).reshape(1, -1)
        
        # Make a prediction using the loaded model
        prediction = model.predict(features_array)
        
        logger.info(f"Prediction made: {prediction}")
        return {"prediction": prediction.tolist()}
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to make prediction")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
