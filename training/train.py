"""
Training script for Plant Disease Detection using PlantDoc dataset
Unified PyTorch pipeline with EfficientNetB0
"""
import os
import sys
import json
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.model import build_model
from backend.config import NUM_CLASSES, IMG_SIZE, MODEL_PATH, CLASSES_PATH
from training.dataset import create_dataloaders


class Trainer:
    """Training wrapper for plant disease classifier"""
    
    def __init__(
        self,
        model: nn.Module,
        device: torch.device,
        learning_rate: float = 1e-3,
        num_classes: int = NUM_CLASSES
    ):
        """
        Initialize trainer
        
        Args:
            model: PyTorch model
            device: Device to train on
            learning_rate: Learning rate
            num_classes: Number of classes
        """
        self.model = model
        self.device = device
        self.num_classes = num_classes
        
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='max', factor=0.5, patience=3, min_lr=1e-6
        )
        
        # Tracking
        self.best_val_acc = 0.0
        self.train_history = {
            'loss': [], 'acc': [],
            'val_loss': [], 'val_acc': []
        }
    
    def train_epoch(self, train_loader) -> tuple:
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(train_loader, desc="Training", leave=False)
        for images, labels in pbar:
            images, labels = images.to(self.device), labels.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            logits = self.model(images)
            loss = self.criterion(logits, labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Metrics
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(logits, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100*correct/total:.2f}%'
            })
        
        epoch_loss = running_loss / total
        epoch_acc = correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, val_loader) -> tuple:
        """Validate the model"""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            pbar = tqdm(val_loader, desc="Validating", leave=False)
            for images, labels in pbar:
                images, labels = images.to(self.device), labels.to(self.device)
                
                logits = self.model(images)
                loss = self.criterion(logits, labels)
                
                running_loss += loss.item() * images.size(0)
                _, predicted = torch.max(logits, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / total
        epoch_acc = correct / total
        
        return epoch_loss, epoch_acc
    
    def save_checkpoint(self, class_names: list):
        """Save model checkpoint"""
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model state
        torch.save(self.model.state_dict(), MODEL_PATH)
        print(f"✓ Model saved to {MODEL_PATH}")
        
        # Save class names
        class_names_dict = {str(i): name for i, name in enumerate(class_names)}
        with open(CLASSES_PATH, 'w') as f:
            json.dump(class_names_dict, f, indent=2)
        print(f"✓ Class names saved to {CLASSES_PATH}")
    
    def train(
        self,
        train_loader,
        val_loader,
        epochs: int = 20,
        class_names: list = None
    ):
        """
        Full training loop
        
        Args:
            train_loader: Training DataLoader
            val_loader: Validation DataLoader
            epochs: Number of epochs
            class_names: List of class names
        """
        print("\n" + "="*70)
        print("🌱 Starting Training - Plant Disease Detection")
        print("="*70)
        print(f"Device: {self.device}")
        print(f"Model: EfficientNetB0")
        print(f"Epochs: {epochs}")
        print(f"Classes: {self.num_classes}")
        print("="*70 + "\n")
        
        for epoch in range(1, epochs + 1):
            print(f"\n[Epoch {epoch}/{epochs}]")
            
            # Train
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # Validate
            val_loss, val_acc = self.validate(val_loader)
            
            # Update history
            self.train_history['loss'].append(train_loss)
            self.train_history['acc'].append(train_acc)
            self.train_history['val_loss'].append(val_loss)
            self.train_history['val_acc'].append(val_acc)
            
            # Print metrics
            print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
            print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f}")
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                print(f"✓ New best model! Val Acc: {val_acc:.4f}")
                if class_names:
                    self.save_checkpoint(class_names)
            
            # Update learning rate
            self.scheduler.step(val_acc)
        
        print("\n" + "="*70)
        print(f"✓ Training Complete! Best Val Acc: {self.best_val_acc:.4f}")
        print("="*70 + "\n")


def main():
    """Main training function"""
    # Configuration
    DATA_ROOT = "data/PlantDoc-Dataset-master"
    BATCH_SIZE = 32
    EPOCHS = 15
    LEARNING_RATE = 1e-3
    NUM_WORKERS = 4
    
    # Check if data exists
    if not Path(DATA_ROOT).exists():
        print(f"❌ Dataset not found at {DATA_ROOT}")
        print("Please ensure PlantDoc dataset is in data/PlantDoc-Dataset-master/")
        return
    
    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n📱 Using device: {device}\n")
    
    # Load data
    print("📂 Loading dataset...")
    train_loader, test_loader = create_dataloaders(
        DATA_ROOT,
        batch_size=BATCH_SIZE,
        img_size=IMG_SIZE,
        num_workers=NUM_WORKERS
    )
    
    # Get class names
    train_dataset = train_loader.dataset
    class_names = train_dataset.get_class_names()
    num_classes = len(class_names)
    
    print(f"✓ Loaded {len(train_dataset)} training samples")
    print(f"✓ {len(test_loader.dataset)} test samples")
    print(f"✓ {num_classes} disease classes")
    
    # Class distribution
    dist = train_dataset.get_class_distribution()
    print(f"✓ Class distribution:")
    for cls, count in sorted(dist.items())[:5]:
        print(f"  - {cls}: {count} images")
    if len(dist) > 5:
        print(f"  ... and {len(dist) - 5} more classes")
    
    # Build model
    print("\n🔧 Building model...")
    model = build_model(num_classes=num_classes)
    model = model.to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"✓ Total parameters: {total_params:,}")
    print(f"✓ Trainable parameters: {trainable_params:,}")
    
    # Train
    trainer = Trainer(
        model=model,
        device=device,
        learning_rate=LEARNING_RATE,
        num_classes=num_classes
    )
    
    trainer.train(
        train_loader=train_loader,
        val_loader=test_loader,  # Use test_loader as validation
        epochs=EPOCHS,
        class_names=class_names
    )
    
    print("\n✅ Training pipeline complete!")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Classes saved to: {CLASSES_PATH}")


if __name__ == "__main__":
    main()
