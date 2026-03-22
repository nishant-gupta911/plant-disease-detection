"""
Utility functions for image preprocessing and handling
"""
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from io import BytesIO
from typing import Tuple

from .config import IMG_SIZE, IMAGENET_MEAN, IMAGENET_STD


def is_likely_plant_leaf(image: Image.Image) -> bool:
    """
    Basic heuristic to check if image likely contains a plant leaf
    Checks for presence of green/brown colors typical of leaves
    
    Args:
        image: PIL Image
    
    Returns:
        True if image likely contains a plant leaf, False otherwise
    """
    # Convert to numpy array
    img_array = np.array(image)
    
    if img_array.size == 0:
        return False
    
    # Normalize to 0-1 range if needed
    if img_array.dtype != np.float32:
        img_array = img_array.astype(np.float32) / 255.0
    
    # Separate RGB channels
    if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
    else:
        return False
    
    # Calculate color ratios
    # Plant leaves typically have higher green channel than red/blue
    green_prominent = (g > r) & (g > b)
    green_ratio = np.sum(green_prominent) / (img_array.shape[0] * img_array.shape[1])
    
    # Leaves also have decent red/brown for edges and veins
    brown_prominent = (r > b) & (r * 0.8 < g)  # Brownish but still greenish
    brown_ratio = np.sum(brown_prominent) / (img_array.shape[0] * img_array.shape[1])
    
    # Photos that are mostly one color (Batman red background) fail this check
    max_single_color = max(
        np.sum(r > 0.7) / (img_array.shape[0] * img_array.shape[1]),
        np.sum(g > 0.7) / (img_array.shape[0] * img_array.shape[1]),
        np.sum(b > 0.7) / (img_array.shape[0] * img_array.shape[1])
    )
    
    # Likely a leaf if:
    # - Has significant green pixels (>15%)
    # - Doesn't have massive single-color dominance (>70% one color = probably not a leaf)
    is_leaf = (green_ratio > 0.15) and (max_single_color < 0.70)
    
    return is_leaf


# Preprocessing transforms (same as training)
def get_inference_transforms():
    """Get transforms for inference (no augmentation)"""
    return transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """
    Load an image from bytes
    
    Args:
        image_bytes: Image data as bytes
    
    Returns:
        PIL Image
    """
    image = Image.open(BytesIO(image_bytes))
    
    # Convert RGBA to RGB
    if image.mode == "RGBA":
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        image = rgb_image
    
    # Convert grayscale to RGB
    elif image.mode != "RGB":
        image = image.convert("RGB")
    
    return image


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Preprocess image for model inference
    
    Args:
        image: PIL Image
    
    Returns:
        Preprocessed tensor of shape (1, 3, 224, 224)
    """
    transforms_fn = get_inference_transforms()
    tensor = transforms_fn(image)
    
    # Add batch dimension
    tensor = tensor.unsqueeze(0)
    
    return tensor


def get_top_k_predictions(
    logits: torch.Tensor,
    class_names: list,
    k: int = 5
) -> list:
    """
    Get top-k predictions from model logits
    
    Args:
        logits: Model output logits of shape (batch_size, num_classes)
        class_names: List of class names
        k: Number of top predictions to return
    
    Returns:
        List of [class_name, confidence] pairs
    """
    # Get probabilities
    probs = torch.softmax(logits, dim=1)[0]
    
    # Get top-k
    top_k_probs, top_k_indices = torch.topk(probs, k=min(k, len(class_names)))
    
    # Convert to Python
    predictions = [
        [class_names[idx.item()], float(prob.item())]
        for idx, prob in zip(top_k_indices, top_k_probs)
    ]
    
    return predictions
