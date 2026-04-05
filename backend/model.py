"""
PyTorch model architecture for Plant Disease Detection
Uses ResNet50 with attention mechanism and optimized classifier head
Better for plant disease detection task
"""
import torch
import torch.nn as nn
from torchvision import models


class AttentionBlock(nn.Module):
    """Channel attention mechanism"""
    def __init__(self, in_channels, reduction=16):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction),
            nn.ReLU(),
            nn.Linear(in_channels // reduction, in_channels),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        b, c, _, _ = x.size()
        avg_y = self.avg_pool(x).view(b, c)
        max_y = self.max_pool(x).view(b, c)
        y = self.fc(avg_y + max_y)
        return x * y.view(b, c, 1, 1)


class PlantDiseaseClassifier(nn.Module):
    """
    ResNet50 backbone with attention and optimized classifier head
    Input: 256x256 RGB images
    Output: num_classes predictions
    Better for plant disease detection
    """
    
    def __init__(self, num_classes: int = 114):
        super().__init__()
        
        # Load pretrained ResNet50 (stronger model than EfficientNet)
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        
        # Freeze earlier layers for fine-tuning
        for param in list(self.backbone.parameters())[:-30]:
            param.requires_grad = False
        
        # Replace average pooling and classifier
        num_features = self.backbone.fc.in_features
        
        # Remove original fc layer
        self.backbone.fc = nn.Identity()
        
        # Add attention
        self.attention = AttentionBlock(num_features)
        
        # New classifier head with heavy regularization
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.6),
            nn.Linear(num_features, 2048),
            nn.BatchNorm1d(2048),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(2048, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(p=0.4),
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model"""
        # Get features from backbone (ResNet without fc)
        x = self.backbone.conv1(x)
        x = self.backbone.bn1(x)
        x = self.backbone.relu(x)
        x = self.backbone.maxpool(x)
        
        x = self.backbone.layer1(x)
        x = self.backbone.layer2(x)
        x = self.backbone.layer3(x)
        x = self.backbone.layer4(x)
        
        # Apply attention
        x = self.attention(x)
        
        # Global average pooling
        x = torch.nn.functional.adaptive_avg_pool2d(x, 1)
        x = torch.flatten(x, 1)
        
        # Classifier
        x = self.classifier(x)
        
        return x


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
