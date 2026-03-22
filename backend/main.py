"""
Production-grade FastAPI backend for Plant Disease Detection
Unified PyTorch inference engine
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Any

from .inference import PredictionEngine
from .config import CORS_ORIGINS, API_HOST, API_PORT


# Initialize FastAPI app
app = FastAPI(
    title="Plant Disease Detection API",
    description="EfficientNetB0-based REST API for detecting plant diseases",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global prediction engine (loaded once)
prediction_engine = None


@app.on_event("startup")
async def startup_event():
    """Initialize prediction engine on startup"""
    global prediction_engine
    try:
        print("\n🌱 Starting Plant Disease Detection API...")
        prediction_engine = PredictionEngine()
        print("✓ Server ready for predictions!\n")
    except Exception as e:
        print(f"✗ Error during startup: {e}")
        raise


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API info"""
    return {
        "message": "Plant Disease Detection API v2.0",
        "framework": "PyTorch + FastAPI",
        "model": "EfficientNetB0",
        "classes": "114 plant diseases",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    if prediction_engine is None or prediction_engine.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "model_loaded": True}


@app.get("/classes")
async def get_classes() -> Dict[str, List[str]]:
    """Get all supported plant disease classes"""
    if prediction_engine is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return {"classes": prediction_engine.get_classes()}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Predict disease on an uploaded plant image
    
    Args:
        file: Image file (PNG, JPG, etc.)
    
    Returns:
        JSON with predicted class and top-5 predictions
    
    Example response:
    {
        "predicted_class": "Tomato_Late_Blight",
        "confidence": 0.95,
        "top_5": [
            ["Tomato_Late_Blight", 0.95],
            ["Tomato_Early_Blight", 0.03],
            ...
        ]
    }
    """
    if prediction_engine is None or prediction_engine.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Get prediction
        result = prediction_engine.predict(image_bytes)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )
