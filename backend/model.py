"""
PyTorch model architecture for Plant Disease Detection
Uses EfficientNetB0 with custom classification head
Matches the training architecture in train.py
"""
import torch
import torch.nn as nn
import timm


class PlantDiseaseClassifier(nn.Module):
    """
    EfficientNetB0 backbone with custom classifier head
    Input: 224x224 RGB images
    Output: num_classes predictions
    """
    
    def __init__(self, num_classes: int = 28, pretrained: bool = True):
        super().__init__()
        
        # Load pretrained EfficientNetB0
        self.backbone = timm.create_model(
            "efficientnet_b0",
            pretrained=pretrained,
            num_classes=0,
            global_pool="avg",
        )
        
        # Get feature dimension from backbone
        feature_dim = self.backbone.num_features
        
        # Custom classifier head (matches training architecture)
        self.head = nn.Sequential(
            nn.BatchNorm1d(feature_dim),
            nn.Dropout(0.3),
            nn.Linear(feature_dim, 256),
            nn.SiLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.15),
            nn.Linear(256, num_classes),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model"""
        # Get features from backbone
        x = self.backbone(x)
        
        # Pass through classification head
        x = self.head(x)
        
        return x


def build_model(num_classes: int = 28, pretrained: bool = True) -> PlantDiseaseClassifier:
    """
    Build and return the plant disease classifier model
    
    Args:
        num_classes: Number of disease classes
        pretrained: Whether to use pretrained weights
    
    Returns:
        Model instance
    """
    model = PlantDiseaseClassifier(num_classes=num_classes, pretrained=pretrained)
    return model
