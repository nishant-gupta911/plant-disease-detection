"""
Custom PyTorch Dataset for PlantDoc
Loads images from directory structure (train/class_name/)
"""
import os
from pathlib import Path
from typing import Tuple, Dict, List, Optional

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from PIL import Image

from .transforms import get_train_transforms, get_val_transforms


class PlantDiseaseDataset(Dataset):
    """
    PyTorch Dataset for PlantDoc plant disease detection
    Uses ImageFolder for simplicity
    
    Expects directory structure:
    data/plantdoc/
    ├── train/
    │   ├── Apple leaf/
    │   ├── Apple Scab Leaf/
    │   └── ...
    └── test/
        ├── Apple leaf/
        └── ...
    """
    
    def __init__(
        self,
        root_dir: str,
        split: str = "train",
        img_size: int = 224,
        augment: bool = True
    ):
        """
        Args:
            root_dir: Root directory containing 'train' and 'test' folders
            split: 'train' or 'test'
            img_size: Image size for resizing
            augment: Whether to apply augmentations
        """
        self.root_dir = Path(root_dir)
        self.split = split
        self.img_size = img_size
        
        # Use ImageFolder for automatic class detection
        split_dir = self.root_dir / split
        if not split_dir.exists():
            raise FileNotFoundError(f"Split directory not found at {split_dir}")
        
        # Create ImageFolder dataset (handles classes automatically)
        self.imagefolder = ImageFolder(str(split_dir))
        
        # Get class names and mapping
        self.class_names = self.imagefolder.classes
        self.class_to_idx = self.imagefolder.class_to_idx
        
        # Transforms
        if augment:
            self.transform = get_train_transforms(img_size)
        else:
            self.transform = get_val_transforms(img_size)
    
    def __len__(self) -> int:
        """Return dataset size"""
        return len(self.imagefolder)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Get a single sample
        
        Args:
            idx: Index
        
        Returns:
            Tuple of (image tensor, label)
        """
        img, label = self.imagefolder[idx]
        
        # Apply transforms
        if self.transform:
            img = self.transform(img)
        
        return img, label
    
    def get_class_names(self) -> List[str]:
        """Get list of class names in order"""
        return self.class_names
    
    def get_class_distribution(self) -> Dict[str, int]:
        """Get class distribution"""
        dist = {}
        for img_path, label in self.imagefolder.imgs:
            class_name = self.class_names[label]
            dist[class_name] = dist.get(class_name, 0) + 1
        return dist


def create_dataloaders(
    root_dir: str,
    batch_size: int = 32,
    img_size: int = 224,
    num_workers: int = 4,
    train_split: bool = True
) -> Tuple[DataLoader, DataLoader]:
    """
    Create train and test dataloaders for PlantDoc
    
    Args:
        root_dir: Root directory of PlantDoc dataset
        batch_size: Batch size
        img_size: Image size
        num_workers: Number of workers for data loading
        train_split: If True, return (train, test). If False, return (test, test)
    
    Returns:
        Tuple of (train_loader, test_loader)
    """
    if train_split:
        train_dataset = PlantDiseaseDataset(
            root_dir, split="train", img_size=img_size, augment=True
        )
    else:
        train_dataset = PlantDiseaseDataset(
            root_dir, split="test", img_size=img_size, augment=False
        )
    
    test_dataset = PlantDiseaseDataset(
        root_dir, split="test", img_size=img_size, augment=False
    )
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, test_loader
