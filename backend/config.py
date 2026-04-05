"""
Configuration for Plant Disease Detection Backend
"""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "model.pt"
CLASSES_PATH = MODEL_DIR / "classes.json"

# Model configuration
IMG_SIZE = 256  # Updated for better feature extraction
DEVICE = "cpu"  # Use CPU for inference (model trained on CPU)
NUM_CLASSES = 28  # PlantDoc dataset

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://localhost:8080"]

# Inference
TOP_K = 5
CONFIDENCE_THRESHOLD = 0.0

# ImageNet normalization (used by torchvision models)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
