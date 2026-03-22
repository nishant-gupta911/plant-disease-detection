"""
Inference engine for Plant Disease Detection
Handles model loading, prediction, and result formatting
"""
import json
import torch
from pathlib import Path
from typing import Dict, List, Any

from .model import build_model
from .utils import load_image_from_bytes, preprocess_image, get_top_k_predictions, is_likely_plant_leaf
from .config import MODEL_PATH, CLASSES_PATH, DEVICE, NUM_CLASSES, TOP_K


class PredictionEngine:
    """
    Singleton inference engine for plant disease detection
    Loads model once and reuses for predictions
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.device = torch.device(DEVICE)
        self.model = None
        self.class_names = None
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load model and class names from disk"""
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        if not CLASSES_PATH.exists():
            raise FileNotFoundError(f"Class names not found at {CLASSES_PATH}")
        
        print(f"📥 Loading model from {MODEL_PATH}...")
        self.model = build_model(num_classes=NUM_CLASSES)
        checkpoint = torch.load(MODEL_PATH, map_location=self.device)
        self.model.load_state_dict(checkpoint)
        self.model = self.model.to(self.device)
        self.model.eval()
        print("✓ Model loaded successfully")
        
        print(f"📂 Loading class names from {CLASSES_PATH}...")
        with open(CLASSES_PATH, 'r') as f:
            classes_dict = json.load(f)
        
        # Convert dict {id: name} to list ordered by id
        if isinstance(classes_dict, dict):
            self.class_names = [classes_dict[str(i)] for i in range(len(classes_dict))]
        else:
            self.class_names = classes_dict
        
        print(f"✓ Loaded {len(self.class_names)} classes")
    
    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Predict disease from image bytes
        
        Args:
            image_bytes: Image data as bytes
        
        Returns:
            Dictionary with predictions
        """
        # Load image
        image = load_image_from_bytes(image_bytes)
        
        # Check if image looks like a plant leaf
        if not is_likely_plant_leaf(image):
            return {
                "error": "Image validation failed",
                "message": "This doesn't look like a plant leaf. Please upload a clear image of a leaf.",
                "predicted_class": None,
                "confidence": 0.0,
                "top_5": []
            }
        
        # Preprocess and prepare for model
        tensor = preprocess_image(image)
        tensor = tensor.to(self.device)
        
        # Inference
        with torch.no_grad():
            logits = self.model(tensor)
        
        # Get predictions
        top_k = get_top_k_predictions(logits, self.class_names, k=TOP_K)
        predicted_class = top_k[0][0]
        confidence = top_k[0][1]
        
        # Reject low confidence predictions (likely out-of-distribution)
        if confidence < 0.40:
            return {
                "error": "Low confidence",
                "message": f"Low confidence prediction ({confidence*100:.1f}%). Image may not be a healthy plant leaf or the disease is unclear.",
                "predicted_class": None,
                "confidence": confidence,
                "top_5": top_k
            }
        
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4),
            "top_5": top_k
        }
    
    def get_classes(self) -> List[str]:
        """Get list of all supported disease classes"""
        return self.class_names
