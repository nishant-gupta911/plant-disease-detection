"""
Model Evaluation Script
Evaluates the trained plant disease detection model on test dataset
"""
import os
import sys
import json
import torch
import numpy as np
from pathlib import Path
from tqdm import tqdm
from torch.utils.data import DataLoader

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.model import build_model
from backend.config import MODEL_PATH, CLASSES_PATH, IMG_SIZE, DEVICE
from training.dataset import PlantDiseaseDataset
from training.transforms import get_val_transforms


class ModelEvaluator:
    """Evaluate plant disease classifier"""
    
    def __init__(self, model_path: str, classes_path: str, device: str = "cpu"):
        """
        Initialize evaluator
        
        Args:
            model_path: Path to saved model
            classes_path: Path to classes JSON
            device: Device to evaluate on
        """
        self.device = torch.device(device)
        self.model_path = model_path
        self.classes_path = classes_path
        
        # Load classes
        with open(classes_path, 'r') as f:
            classes_dict = json.load(f)
            self.classes = [classes_dict[str(i)] for i in range(len(classes_dict))]
        
        num_classes = len(self.classes)
        
        # Build and load model
        self.model = build_model(num_classes=num_classes)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()
        
        print(f"✓ Model loaded from {model_path}")
        print(f"✓ {num_classes} disease classes")
    
    def evaluate(self, test_loader: DataLoader):
        """
        Evaluate model on test set
        
        Args:
            test_loader: Test DataLoader
        
        Returns:
            Dictionary with evaluation metrics
        """
        correct = 0
        total = 0
        class_correct = {cls: 0 for cls in self.classes}
        class_total = {cls: 0 for cls in self.classes}
        
        print("\n📊 EVALUATING MODEL ON TEST SET")
        print("=" * 70)
        
        with torch.no_grad():
            pbar = tqdm(test_loader, desc="Evaluating", leave=True)
            for images, labels in pbar:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                # Forward pass
                logits = self.model(images)
                _, predicted = torch.max(logits, 1)
                
                # Update total
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                # Update per-class accuracy
                for label, pred in zip(labels, predicted):
                    class_name = self.classes[label.item()]
                    class_total[class_name] += 1
                    if label == pred:
                        class_correct[class_name] += 1
                
                pbar.set_postfix({'Accuracy': f'{100*correct/total:.2f}%'})
        
        # Calculate overall accuracy
        overall_acc = correct / total
        
        print("\n" + "=" * 70)
        print(f"✓ OVERALL ACCURACY: {overall_acc:.4f} ({100*overall_acc:.2f}%)")
        print("=" * 70)
        
        # Per-class accuracy
        print("\n📈 PER-CLASS ACCURACY:")
        print("-" * 70)
        print(f"{'Class':<45} {'Accuracy':<15} {'Count'}")
        print("-" * 70)
        
        per_class_acc = {}
        for class_name in sorted(self.classes):
            if class_total[class_name] > 0:
                acc = class_correct[class_name] / class_total[class_name]
                per_class_acc[class_name] = acc
                print(f"{class_name:<45} {acc:>6.2%}          {class_total[class_name]:>4}")
        
        print("-" * 70)
        
        # Statistics
        accuracies = list(per_class_acc.values())
        print(f"\n📊 STATISTICS:")
        print(f"   Mean Accuracy: {np.mean(accuracies):.4f}")
        print(f"   Std Dev: {np.std(accuracies):.4f}")
        print(f"   Min Accuracy: {np.min(accuracies):.4f}")
        print(f"   Max Accuracy: {np.max(accuracies):.4f}")
        
        return {
            'overall_accuracy': overall_acc,
            'per_class_accuracy': per_class_acc,
            'total_samples': total,
            'correct_predictions': correct
        }
    
    def predict_sample(self, image_path: str):
        """
        Predict disease for a single image
        
        Args:
            image_path: Path to image file
        
        Returns:
            Prediction results
        """
        from PIL import Image
        
        # Load and preprocess image
        img = Image.open(image_path)
        transform = get_val_transforms(IMG_SIZE)
        img_tensor = transform(img).unsqueeze(0).to(self.device)
        
        # Predict
        with torch.no_grad():
            logits = self.model(img_tensor)
            probs = torch.softmax(logits, dim=1)
            top_probs, top_indices = torch.topk(probs, 3)
        
        results = {
            'image': image_path,
            'top_predictions': [
                {
                    'class': self.classes[top_indices[0][i].item()],
                    'confidence': top_probs[0][i].item()
                }
                for i in range(3)
            ]
        }
        
        return results


def main():
    """Main evaluation function"""
    
    print("\n" + "=" * 70)
    print("🌿 PLANT DISEASE DETECTION - MODEL EVALUATION")
    print("=" * 70 + "\n")
    
    # Check if model exists
    if not Path(MODEL_PATH).exists():
        print(f"❌ Model not found at {MODEL_PATH}")
        print("Please train the model first: python training/train.py")
        return
    
    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"📱 Using device: {device}\n")
    
    # Initialize evaluator
    evaluator = ModelEvaluator(
        model_path=str(MODEL_PATH),
        classes_path=str(CLASSES_PATH),
        device=str(device)
    )
    
    # Load test dataset
    dataset_root = "data/PlantDoc-Dataset-master"
    if not Path(dataset_root).exists():
        print(f"❌ Dataset not found at {dataset_root}")
        return
    
    print("📂 Loading test dataset...")
    test_dataset = PlantDiseaseDataset(
        root_dir=dataset_root,
        split="test",
        img_size=IMG_SIZE,
        augment=False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=4
    )
    
    print(f"✓ Loaded {len(test_dataset)} test images")
    
    # Evaluate
    results = evaluator.evaluate(test_loader)
    
    print("\n" + "=" * 70)
    print("✅ EVALUATION COMPLETE")
    print("=" * 70 + "\n")
    
    return results


if __name__ == "__main__":
    main()
