# Plant Disease Detection System

An AI-powered plant disease detection system using deep learning. Upload a leaf photo to instantly identify diseases across 28 plant species with 58% accuracy.

## 🌟 Features

- **AI Inference**: EfficientNetB0 CNN trained on 2,300+ leaf images
- **28 Disease Classes**: Supports 28 different plant diseases and healthy states
- **Fast Predictions**: Real-time classification with confidence scoring
- **Leaf Validation**: Automatic leaf detection to prevent false classifications
- **Modern UI**: React frontend with responsive design
- **REST API**: FastAPI backend for easy integration

## 🏗️ Architecture

```
project/
├── backend/              # FastAPI inference server (port 8001)
│   ├── main.py          # REST API endpoints
│   ├── model.py         # EfficientNetB0 architecture
│   ├── inference.py     # Prediction engine
│   ├── config.py        # Configuration
│   └── utils.py         # Leaf validation
├── frontend/            # React + Vite application (port 5174)
│   ├── src/
│   │   ├── components/  # Hero, ImageUploader, ResultCard, ClassesGrid
│   │   └── App.jsx      # Main application
│   └── tailwind.config.js
├── training/            # Model training pipeline
│   ├── train.py         # Training script
│   ├── dataset.py       # Data loading
│   ├── evaluation.py    # Model evaluation
│   └── transforms.py    # Data augmentation
├── experiment/          # Jupyter notebooks for exploration
│   └── 5 analysis notebooks
├── models/              # Trained model artifacts
│   ├── model.pt         # Trained weights (18MB)
│   └── classes.json     # Class definitions
└── main.py             # Orchestrator script
```

## 📊 Model Performance

- **Test Accuracy**: 58.05%
- **Training Epochs**: 15
- **Dataset**: PlantDoc (2,336 training, 236 test samples)
- **Architecture**: EfficientNetB0 → 512 hidden → 28 classes
- **Confidence Threshold**: 40% (minimum)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip & npm

### Installation

```bash
# Clone and setup
cd plant-disease-detection

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Running the System

**Option 1: Run all components**
```bash
python main.py
```

**Option 2: Run individually**

Backend:
```bash
source .venv/bin/activate
python -m uvicorn backend.main:app --port 8001 --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

### Access Application
- Frontend: http://localhost:5174
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### List Classes
```bash
GET /classes
```

### Make Prediction
```bash
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

## 🎯 Disease Classes

The model detects 28 plant diseases including:
- Apple diseases (Scab, Rust, Healthy)
- Tomato diseases (Early blight, Late blight, Mosaic Virus, Septoria, etc.)
- Corn diseases (Gray leaf spot, Leaf blight, Rust)
- Potato diseases (Early blight, Late blight)
- And more...

## 🔧 Development

### Training Custom Model
```bash
python training/train.py
```

### Model Evaluation
```bash
python -m training.evaluation
```

### Jupyter Experiments
```bash
jupyter notebook experiment/
```

## 📚 Documentation

- [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) - Detailed setup instructions
- [SYSTEM_STATUS.md](SYSTEM_STATUS.md) - Architecture overview
- [FRONTEND_BACKEND_FIXES.md](FRONTEND_BACKEND_FIXES.md) - Debugging solutions
- [experiment/README.md](experiment/README.md) - Experiment details
- [experiment/FINAL_REPORT.md](experiment/FINAL_REPORT.md) - Analysis results

## 🛠️ Tech Stack

**Backend**
- FastAPI - REST API framework
- PyTorch - Deep learning
- Pillow - Image processing
- Python 3.8+

**Frontend**
- React 18 - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Framer Motion - Animations

## 🎓 Training Data

- **Dataset**: PlantDoc + PlantSegV2
- **Training Samples**: 2,336 images
- **Test Samples**: 236 images
- **Classes**: 28
- **Augmentation**: Rotation, flip, color jitter, resize

## 📈 Project Timeline

1. **Data Pipeline** - Dataset integration and augmentation
2. **Model Design** - EfficientNetB0 architecture
3. **Training** - 15 epochs with optimization
4. **Backend API** - FastAPI with inference engine
5. **Frontend** - React UI with predictions
6. **Integration** - Full system testing
7. **Deployment** - Production readiness

## 🤝 Contributing

This is a personal research project. For improvements:
1. Create a branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📝 License

MIT License - See LICENSE file for details

## 📞 Contact

Built by Nishant Gupta  
GitHub: [@nishant-gupta911](https://github.com/nishant-gupta911)

---

**Note**: This system is for research and educational purposes. Always consult agricultural experts for actual disease diagnosis.
