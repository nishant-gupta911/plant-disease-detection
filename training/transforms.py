"""
Data augmentation transforms for training
ImageNet normalization with augmentations
"""
from torchvision import transforms


def get_train_transforms(img_size: int = 224):
    """
    Get augmented transforms for training
    
    Args:
        img_size: Target image size
    
    Returns:
        Compose object with augmentations
    """
    return transforms.Compose([
        transforms.RandomResizedCrop(img_size, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def get_val_transforms(img_size: int = 224):
    """
    Get transforms for validation (no augmentation)
    
    Args:
        img_size: Target image size
    
    Returns:
        Compose object without augmentations
    """
    return transforms.Compose([
        transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
