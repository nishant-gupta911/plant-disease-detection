"""
PyTorch model architecture for Plant Disease Detection
Uses EfficientNetB0 with a lightweight classifier head
"""
import torch
import torch.nn as nn
from torchvision import models


class PlantDiseaseClassifier(nn.Module):
    """
    EfficientNetB0 backbone with custom classifier head
    Input: 224x224 RGB images
    Output: num_classes predictions
    """
    
    def __init__(self, num_classes: int = 114):
        super().__init__()
        
        # Load pretrained EfficientNetB0
        self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        
        # Get feature dimension
        num_features = self.backbone.classifier[1].in_features
        
        # Replace classifier with lightweight head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.4),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model"""
        return self.backbone(x)


def build_model(num_classes: int = 114, pretrained: bool = True) -> PlantDiseaseClassifier:
    """
    Build and return the plant disease classifier model
    
    Args:
        num_classes: Number of disease classes
        pretrained: Whether to use pretrained weights
    
    Returns:
        Model instance
    """
    model = PlantDiseaseClassifier(num_classes=num_classes)
    return model
