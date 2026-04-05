import json
import os
import time
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import timm
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import datasets, transforms
from tqdm import tqdm

warnings.filterwarnings("ignore")


if not torch.backends.mps.is_available():
    raise RuntimeError("MPS is required for this script. Apple Metal device not found.")

device = torch.device("mps")
print(f"Device: {device}")


CONFIG = {
    "model_name": "efficientnet_b0",
    "image_size": 224,
    "batch_size": 64,
    "num_workers": 0,
    "phase1_epochs": 8,
    "phase2_epochs": 22,
    "lr_head": 1e-3,
    "lr_backbone": 3e-5,
    "weight_decay": 1e-4,
    "label_smoothing": 0.1,
    "dropout_rate": 0.3,
    "mixup_prob": 0.4,
    "mixup_alpha": 0.3,
    "patience": 8,
    "use_tta": True,
    "train_path": "data/PlantDoc-Dataset-master/train",
    "test_path": "data/PlantDoc-Dataset-master/test",
    "checkpoint_dir": "checkpoints",
    "best_model_path": "checkpoints/best_model.pth",
    "log_path": "logs/training_log.csv",
    "confusion_matrix_path": "logs/confusion_matrix.png",
    "classes_path": "models/classes.json",
    "top_classes": [
        "Corn leaf blight",
        "Tomato Septoria leaf spot",
        "Squash Powdery mildew leaf",
        "Raspberry leaf",
        "Potato leaf early blight",
        "Corn rust leaf",
        "Blueberry leaf",
        "Peach leaf",
        "Tomato leaf late blight",
        "Tomato leaf bacterial spot",
    ],
    "val_split": 0.15,
    "num_classes": 10,
    "max_minutes": 43,
    "seed": 42,
}

torch.manual_seed(CONFIG["seed"])
np.random.seed(CONFIG["seed"])

if len(CONFIG["top_classes"]) != CONFIG["num_classes"]:
    raise ValueError("top_classes must contain exactly 10 class names.")


train_root = CONFIG["train_path"]
class_counts = {
    cls: len(
        [
            name
            for name in os.listdir(os.path.join(train_root, cls))
            if os.path.isfile(os.path.join(train_root, cls, name))
        ]
    )
    for cls in os.listdir(train_root)
    if os.path.isdir(os.path.join(train_root, cls))
}

missing = [cls for cls in CONFIG["top_classes"] if cls not in class_counts]
if missing:
    raise FileNotFoundError(f"Configured top classes not found in training set: {missing}")

print("\nTop 10 classes selected:")
for idx, cls_name in enumerate(CONFIG["top_classes"]):
    print(f"  {idx}: {cls_name} ({class_counts[cls_name]} images)")


train_transform = transforms.Compose(
    [
        transforms.RandomResizedCrop(CONFIG["image_size"], scale=(0.65, 1.0)),
        transforms.RandomHorizontalFlip(0.5),
        transforms.RandomVerticalFlip(0.2),
        transforms.ColorJitter(0.3, 0.3, 0.3, 0.05),
        transforms.RandomRotation(25),
        transforms.RandomGrayscale(0.05),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        transforms.RandomErasing(p=0.2),
    ]
)

val_transform = transforms.Compose(
    [
        transforms.Resize((CONFIG["image_size"], CONFIG["image_size"])),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


class CustomSubset(Dataset):
    def __init__(self, dataset, indices, class_map, transform):
        self.dataset = dataset
        self.indices = indices
        self.class_map = class_map
        self.transform = transform

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, index):
        path, original_label = self.dataset.samples[self.indices[index]]
        class_name = self.dataset.classes[original_label]
        new_label = self.class_map[class_name]
        image = Image.open(path).convert("RGB")
        return self.transform(image), new_label


def mixup(inputs, targets, alpha=0.3):
    lam = np.random.beta(alpha, alpha)
    indices = torch.randperm(inputs.size(0), device=inputs.device)
    return lam * inputs + (1 - lam) * inputs[indices], targets, targets[indices], lam


def mixup_loss(loss_fn, predictions, targets_a, targets_b, lam):
    return lam * loss_fn(predictions, targets_a) + (1 - lam) * loss_fn(predictions, targets_b)


def train_epoch(loader, optimizer, phase, model, device, criterion):
    model.train()
    loss_sum = 0.0
    correct = 0
    total = 0

    for inputs, targets in tqdm(loader, desc=f"  [{phase}] train", leave=False):
        inputs = inputs.to(device)
        targets = targets.to(device)
        use_mix = np.random.random() < CONFIG["mixup_prob"]

        if use_mix:
            inputs, targets_a, targets_b, lam = mixup(inputs, targets, CONFIG["mixup_alpha"])

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = mixup_loss(criterion, outputs, targets_a, targets_b, lam) if use_mix else criterion(outputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        loss_sum += loss.item()
        if not use_mix:
            predictions = outputs.argmax(1)
            correct += (predictions == targets).sum().item()
            total += targets.size(0)

    return loss_sum / max(len(loader), 1), (correct / total if total else 0.0)


def tta_predict(inputs, model, device):
    variants = [
        inputs,
        inputs.flip(3),
        inputs.flip(2),
        inputs.rot90(1, [2, 3]),
        inputs.rot90(3, [2, 3]),
    ]
    with torch.no_grad():
        probabilities = [torch.softmax(model(variant), dim=1) for variant in variants]
    return torch.stack(probabilities).mean(0)


def validate(loader, model, device, criterion, use_tta=False):
    model.eval()
    loss_sum = 0.0
    predictions = []
    truths = []

    with torch.no_grad():
        for inputs, targets in tqdm(loader, desc="  val", leave=False):
            inputs = inputs.to(device)
            targets = targets.to(device)

            if use_tta:
                probs = tta_predict(inputs, model, device)
                predicted = probs.argmax(1)
            else:
                outputs = model(inputs)
                predicted = outputs.argmax(1)
                loss_sum += criterion(outputs, targets).item()

            predictions.extend(predicted.cpu().tolist())
            truths.extend(targets.cpu().tolist())

    accuracy = float((np.array(predictions) == np.array(truths)).mean())
    average_loss = loss_sum / max(len(loader), 1) if not use_tta else 0.0
    return average_loss, accuracy, predictions, truths


def save_confusion_matrix(true_labels, pred_labels):
    matrix = confusion_matrix(true_labels, pred_labels)
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        xticklabels=CONFIG["top_classes"],
        yticklabels=CONFIG["top_classes"],
    )
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Test Confusion Matrix")
    plt.tight_layout()
    plt.savefig(CONFIG["confusion_matrix_path"], dpi=200)
    plt.close()


if __name__ == "__main__":
    full_train = datasets.ImageFolder(CONFIG["train_path"])
    kept = {class_name: idx for idx, class_name in enumerate(CONFIG["top_classes"])}
    valid_indices = [
        index
        for index, (_, label) in enumerate(full_train.samples)
        if full_train.classes[label] in kept
    ]
    labels_all = [kept[full_train.classes[full_train.samples[index][1]]] for index in valid_indices]

    train_indices, val_indices = train_test_split(
        valid_indices,
        test_size=CONFIG["val_split"],
        stratify=labels_all,
        random_state=CONFIG["seed"],
    )

    train_ds = CustomSubset(full_train, train_indices, kept, train_transform)
    val_ds = CustomSubset(full_train, val_indices, kept, val_transform)

    train_labels = [kept[full_train.classes[full_train.samples[index][1]]] for index in train_indices]
    class_weights = compute_class_weight("balanced", classes=np.arange(CONFIG["num_classes"]), y=train_labels)
    class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32, device=device)
    criterion = nn.CrossEntropyLoss(
        weight=class_weights_tensor,
        label_smoothing=CONFIG["label_smoothing"],
    )

    sample_weights = [class_weights[label] for label in train_labels]
    sampler = WeightedRandomSampler(sample_weights, len(sample_weights), replacement=True)

    loader_kwargs = {
        "batch_size": CONFIG["batch_size"],
        "num_workers": CONFIG["num_workers"],
        "pin_memory": False,
    }

    train_loader = DataLoader(train_ds, sampler=sampler, **loader_kwargs)
    val_loader = DataLoader(val_ds, shuffle=False, **loader_kwargs)

    test_full = datasets.ImageFolder(CONFIG["test_path"])
    test_indices = [
        index
        for index, (_, label) in enumerate(test_full.samples)
        if test_full.classes[label] in kept
    ]
    test_ds = CustomSubset(test_full, test_indices, kept, val_transform)
    test_loader = DataLoader(test_ds, shuffle=False, **loader_kwargs)

    print(f"\nTrain: {len(train_ds)} | Val: {len(val_ds)} | Test: {len(test_ds)}")

    os.makedirs(CONFIG["checkpoint_dir"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    backbone = timm.create_model(
        CONFIG["model_name"],
        pretrained=True,
        num_classes=0,
        global_pool="avg",
    )
    feature_dim = backbone.num_features

    head = nn.Sequential(
        nn.BatchNorm1d(feature_dim),
        nn.Dropout(CONFIG["dropout_rate"]),
        nn.Linear(feature_dim, 256),
        nn.SiLU(),
        nn.BatchNorm1d(256),
        nn.Dropout(CONFIG["dropout_rate"] * 0.5),
        nn.Linear(256, CONFIG["num_classes"]),
    )

    model = nn.Sequential(backbone, head).to(device)
    print(f"Model: {CONFIG['model_name']} | Params: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")

    best_acc = 0.0
    no_improve = 0
    log_rows = []
    start = time.time()

    for param in backbone.parameters():
        param.requires_grad = False

    optimizer_phase1 = torch.optim.AdamW(
        head.parameters(),
        lr=CONFIG["lr_head"],
        weight_decay=CONFIG["weight_decay"],
    )
    scheduler_phase1 = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer_phase1,
        T_max=CONFIG["phase1_epochs"],
    )

    print("\n=== PHASE 1: Head only ===")
    for epoch in range(1, CONFIG["phase1_epochs"] + 1):
        train_loss, train_acc = train_epoch(train_loader, optimizer_phase1, "P1", model, device, criterion)
        val_loss, val_acc, _, _ = validate(val_loader, model, device, criterion)
        scheduler_phase1.step()
        elapsed = (time.time() - start) / 60
        print(f"Ep {epoch:02d} | tr {train_acc:.3f} | val {val_acc:.3f} | {elapsed:.1f}min elapsed")
        log_rows.append([epoch, "P1", train_loss, train_acc, val_loss, val_acc])
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), CONFIG["best_model_path"])

    for param in backbone.parameters():
        param.requires_grad = True

    optimizer_phase2 = torch.optim.AdamW(
        [
            {"params": backbone.parameters(), "lr": CONFIG["lr_backbone"]},
            {"params": head.parameters(), "lr": CONFIG["lr_head"] * 0.1},
        ],
        weight_decay=CONFIG["weight_decay"],
    )
    scheduler_phase2 = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer_phase2,
        T_0=10,
        T_mult=2,
        eta_min=1e-7,
    )

    print("\n=== PHASE 2: Full fine-tune ===")
    for epoch in range(CONFIG["phase1_epochs"] + 1, CONFIG["phase1_epochs"] + CONFIG["phase2_epochs"] + 1):
        elapsed = (time.time() - start) / 60
        if elapsed > CONFIG["max_minutes"]:
            print(f"Time limit hit at epoch {epoch}. Stopping.")
            break

        train_loss, train_acc = train_epoch(train_loader, optimizer_phase2, "P2", model, device, criterion)
        val_loss, val_acc, _, _ = validate(val_loader, model, device, criterion)
        scheduler_phase2.step()
        print(f"Ep {epoch:02d} | tr {train_acc:.3f} | val {val_acc:.3f} | {elapsed:.1f}min elapsed")
        log_rows.append([epoch, "P2", train_loss, train_acc, val_loss, val_acc])

        if val_acc > best_acc:
            best_acc = val_acc
            no_improve = 0
            torch.save(model.state_dict(), CONFIG["best_model_path"])
            print(f"  Best: {best_acc:.4f}")
        else:
            no_improve += 1
            if no_improve >= CONFIG["patience"]:
                print("Early stopping triggered.")
                break

    pd.DataFrame(
        log_rows,
        columns=["ep", "phase", "tr_loss", "tr_acc", "val_loss", "val_acc"],
    ).to_csv(CONFIG["log_path"], index=False)

    model.load_state_dict(torch.load(CONFIG["best_model_path"], map_location=device))
    _, test_acc, test_preds, test_labels = validate(test_loader, model, device, criterion, use_tta=CONFIG["use_tta"])
    print(f"\nTest Accuracy (TTA): {test_acc:.4f}")
    print(classification_report(test_labels, test_preds, target_names=CONFIG["top_classes"], digits=3))

    save_confusion_matrix(test_labels, test_preds)

    with open(CONFIG["classes_path"], "w", encoding="utf-8") as handle:
        json.dump(CONFIG["top_classes"], handle, indent=2)

    print(f"Classes saved -> {CONFIG['classes_path']}")
    print(f"Confusion matrix saved -> {CONFIG['confusion_matrix_path']}")
    print(f"Total time: {(time.time() - start) / 60:.1f} min")
    print("OK")
