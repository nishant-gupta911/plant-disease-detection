# Plant Disease Detection System

A deep learning-based plant disease detection application using EfficientNetB0 transfer learning, FastAPI backend, and React frontend.

## 🎯 Project Overview

This project detects 10 distinct plant diseases from leaf images using a pre-trained EfficientNetB0 model with custom fine-tuning. The system consists of:

- **ML Pipeline:** TensorFlow/Keras with PyTorch training and MPS GPU acceleration
- **Backend:** FastAPI REST API for inference
- **Frontend:** React 18 with Vite (responsive, dark theme)
- **Dataset:** PlantDoc Dataset (1000 training images across 10 classes)

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Test Accuracy (TTA)** | **80.65%** |
| **Best Validation Accuracy** | 72.32% |
| **Training Time** | 84.9 minutes (MPS GPU) |
| **Model Architecture** | EfficientNetB0 + Custom Head |
| **Total Parameters** | 4.3M |

### Per-Class Performance (Test Set)

| Disease Class | Precision | Recall | F1-Score | Support |
|---------------|-----------|--------|----------|---------|
| Corn leaf blight | 1.000 | 1.000 | 1.000 | 12 |
| Corn rust leaf | 1.000 | 1.000 | 1.000 | 10 |
| Squash Powdery mildew leaf | 1.000 | 0.667 | 0.800 | 6 |
| Peach leaf | 0.900 | 1.000 | 0.947 | 9 |
| Raspberry leaf | 0.875 | 1.000 | 0.933 | 7 |
| Blueberry leaf | 0.909 | 0.909 | 0.909 | 11 |
| Tomato leaf late blight | 0.857 | 0.600 | 0.706 | 10 |
| Potato leaf early blight | 0.545 | 0.750 | 0.632 | 8 |
| Tomato Septoria leaf spot | 0.600 | 0.545 | 0.571 | 11 |
| Tomato leaf bacterial spot | 0.500 | 0.556 | 0.526 | 9 |

## 🏗️ Project Structure

```
plant_disease_detection/
├── README.md                          # Project documentation
├── train.py                           # Model training pipeline (2-phase)
├── app.py                             # Frontend entry point
├── requirements.txt                   # Main dependencies
├── requirements_local.txt             # Local dev dependencies
├── PlantDisease_Colab.ipynb          # Jupyter notebook version
│
├── backend/                           # FastAPI backend
│   ├── main.py                        # REST API endpoints
│   ├── inference.py                   # Model inference logic
│   ├── model.py                       # Model architecture
│   ├── config.py                      # Configuration
│   ├── utils.py                       # Utility functions
│   ├── requirements.txt               # Backend dependencies
│   └── __init__.py
│
├── data/
│   └── PlantDoc-Dataset-master/      # Training dataset
│       ├── train/                     # 1000 training images (10 classes)
│       └── test/                      # 93 test images
│
├── models/
│   ├── model.pt                       # Trained model weights
│   ├── classes.json                   # Class names mapping
│   └── checkpoints/                   # Model checkpoints
│
├── logs/
│   ├── training_log.csv              # Training metrics
│   └── confusion_matrix.png          # Test set confusion matrix
│
└── checkpoints/
    └── best_model.pth                # Best model checkpoint
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ or 3.14
- macOS with Apple Silicon (M1/M2/M3) for MPS GPU acceleration
- pip or conda package manager

### Installation

1. **Clone the repository:**
```bash
cd /Users/nishant/Documents/vscode/plant_disease_detection
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Training the Model

```bash
python train.py
```

**Training Configuration:**
- **Phase 1:** Head-only training (8 epochs) - Freezes backbone, fine-tunes classification head
- **Phase 2:** Full model fine-tuning (up to 22 epochs) - Unfreezes backbone with lower learning rates
- **GPU Acceleration:** Uses MPS (Metal Performance Shaders) on Mac
- **Time Limit:** 43 minutes (automatic early stopping if exceeded)
- **Early Stopping:** Triggers after 8 epochs without validation improvement

**Training Output:**
- Best model checkpoint: `checkpoints/best_model.pth`
- Training log: `logs/training_log.csv`
- Test confusion matrix: `logs/confusion_matrix.png`
- Class indices: `models/classes.json`

### Running the Backend API

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**API Endpoints:**
- `POST /predict` - Predict disease from uploaded image
- `GET /classes` - Get list of supported disease classes
- `GET /health` - Health check endpoint

**Example Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@leaf_image.jpg"
```

**Example Response:**
```json
{
  "predicted_class": "Corn leaf blight",
  "confidence": 0.9876,
  "top_3_predictions": [
    {"class": "Corn leaf blight", "confidence": 0.9876},
    {"class": "Corn rust leaf", "confidence": 0.0098},
    {"class": "Blueberry leaf", "confidence": 0.0026}
  ]
}
```

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open browser to `http://localhost:5173`

## 🔧 Key Implementation Details

### Data Processing

- **Image Size:** 224×224 pixels
- **Train/Val Split:** 85/15
- **Data Augmentation:**
  - Random resized crops (65-100% scale)
  - Random flips (horizontal: 50%, vertical: 20%)
  - Color jitter (brightness, contrast, saturation, hue)
  - Random rotation (±25°)
  - Random erasing (20% probability)
  - Random grayscale (5% probability)

### Training Strategy

1. **Phase 1:** Train only the classification head
   - Learning rate: 0.001 (head)
   - Optimizer: AdamW
   - Scheduler: CosineAnnealing

2. **Phase 2:** Fine-tune entire network
   - Learning rates: 3e-5 (backbone), 1e-4 (head)
   - Optimizer: AdamW with differential learning rates
   - Scheduler: CosineAnnealingWarmRestarts

### Loss Function

- Cross-entropy loss with class weights (handles class imbalance)
- Label smoothing: 0.1
- Mixup augmentation: 40% probability, α=0.3

### Model Details

- **Base Model:** EfficientNetB0 (pretrained ImageNet)
- **Custom Head:**
  - BatchNorm → Dropout(0.3) → Linear(1280→256) → SiLU → BatchNorm → Dropout(0.15) → Linear(256→10)
- **Total Parameters:** 4.3M

### Performance Optimization

- **MPS GPU Acceleration:** ~0.73 sec/batch (vs 6.61 sec/batch on CPU)
- **Data Loading:** Pin memory disabled for Mac compatibility
- **Batch Size:** 64
- **Training Time:** ~1.4 hours on Mac M-series GPU

## 📈 Training Results

### Training Metrics

```
PHASE 1: Head-only Training (8 epochs)
Epoch 1: Train Acc=51.0%, Val Acc=61.6%
Epoch 2: Train Acc=69.9%, Val Acc=66.1%
Epoch 3: Train Acc=69.5%, Val Acc=69.5%
Epoch 4: Train Acc=76.8%, Val Acc=67.8%
Epoch 5: Train Acc=73.2%, Val Acc=71.2%
Epoch 6: Train Acc=75.0%, Val Acc=71.2%
Epoch 7: Train Acc=77.1%, Val Acc=70.6%
Epoch 8: Train Acc=80.9%, Val Acc=71.8%

PHASE 2: Full Fine-tuning (3 epochs)
Epoch 9:  Train Acc=76.6%, Val Acc=72.3% ⭐ Best
Epoch 10: Train Acc=78.1%, Val Acc=71.8%
Epoch 11: Train Acc=84.2%, Val Acc=72.3%
[Stopped at epoch 12 - 43-minute time limit reached]
```

### Test Set Results

- **Test Accuracy (Test-Time Augmentation):** 80.65%
- **Per-class F1-scores:** Ranging from 0.526 to 1.000
- **Best performing classes:** Corn leaf blight, Corn rust leaf (100% F1)
- **Challenging classes:** Tomato bacterial spot (52.6% F1), Tomato Septoria spot (57.1% F1)

## 🐍 Dependencies

### Core ML Libraries
- torch >= 2.0.0
- torchvision >= 0.15.0
- timm >= 0.9.0 (EfficientNet models)
- numpy, pandas, scikit-learn

### Data Processing
- Pillow (image processing)
- albumentations >= 1.3.0

### Visualization
- matplotlib, seaborn

### Backend
- fastapi, uvicorn
- python-multipart

### Development
- jupyter, ipython
- tqdm (progress bars)

## 💡 Usage Examples

### Inference from Command Line

```python
import torch
from backend.model import load_model
from PIL import Image

# Load model
model = load_model('checkpoints/best_model.pth')

# Load image
image = Image.open('leaf.jpg')

# Get prediction
prediction = model.predict(image)
print(f"Predicted: {prediction['class']} ({prediction['confidence']:.2%})")
```

### Using the API

```python
import requests

response = requests.post(
    'http://localhost:8000/predict',
    files={'file': open('leaf.jpg', 'rb')}
)
result = response.json()
print(result)
```

## 🔍 Troubleshooting

### MPS Device Not Found
- Ensure you're on macOS with Apple Silicon (M1/M2/M3)
- Check: `python -c "import torch; print(torch.backends.mps.is_available())"`

### Out of Memory
- Reduce batch size in CONFIG['batch_size']
- Set num_workers=0 for Mac compatibility

### Slow Training on CPU
- Install PyTorch with CUDA if using NVIDIA GPU
- Use MPS acceleration on Mac

## 📝 License

This project uses the PlantDoc dataset for research and educational purposes.

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Commit with descriptive messages
4. Push to GitHub
5. Create a Pull Request

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Last Updated:** April 5, 2026
**Model Training Completed:** ✅ (80.65% test accuracy)
**Status:** Production Ready
