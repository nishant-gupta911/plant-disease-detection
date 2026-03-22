# 🚀 EXECUTION GUIDE

## Quick Start

### Option 1: Run Everything (Recommended)
```bash
python main.py
```
This will:
1. ✅ Check if model is trained (train if needed)
2. ✅ Start Backend API (port 8001)
3. ✅ Start Frontend (port 5174)
4. ✅ Run Model Evaluation
5. ✅ Display system status

---

## Individual Commands

### Train Model Only
```bash
python main.py --train
# or
python training/train.py
```
**Time:** ~2 hours on CPU, ~30 mins on GPU

---

### Backend Only
```bash
python main.py --backend
```
**Starts:** FastAPI on port 8001  
**Requirements:** Trained model (model.pt)

---

### Frontend Only
```bash
python main.py --frontend
```
**Starts:** React + Vite on port 5174  
**Requirements:** Node.js, npm

---

### Evaluate Model Only
```bash
python main.py --eval
# or
python training/evaluation.py
```
**Tests:** Model on test dataset  
**Output:** Per-class accuracy metrics

---

## Full System Details

### 📊 Evaluation Script (`training/evaluation.py`)

**Features:**
- ✅ Load trained model
- ✅ Evaluate on test dataset (236 images)
- ✅ Calculate overall accuracy
- ✅ Per-class accuracy breakdown
- ✅ Statistical analysis

**Output Example:**
```
Overall Accuracy: 58.05%
Best Classes: Bell Pepper (100%), Raspberry (100%)
Worst Classes: Grape (0%), Spider Mites (0%)
Mean Accuracy: 58.65%
```

**Run:**
```bash
python training/evaluation.py
```

---

### 🎮 Main Orchestration Script (`main.py`)

**Features:**
- ✅ Manage all services
- ✅ Auto-train if model missing
- ✅ Wait for services to be ready
- ✅ Display system status
- ✅ Graceful shutdown (Ctrl+C)

**Usage:**
```bash
python main.py [--train|--backend|--frontend|--eval]
```

**Options:**
```
--train     Train model only
--backend   Run backend API only  
--frontend  Run frontend UI only
--eval      Evaluate model only
(no args)   Run full system
```

---

## 🌐 Access Points

After running `python main.py`:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5174 | Upload images, view predictions |
| **API Docs** | http://localhost:8001/docs | Interactive API explorer |
| **API Base** | http://localhost:8001 | REST API endpoints |

---

## 📊 API Endpoints

### 1. Health Check
```bash
curl http://localhost:8001/health
```
**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

### 2. Get Classes
```bash
curl http://localhost:8001/classes
```
**Response:**
```json
{
  "classes": [
    "Apple leaf",
    "Apple Scab Leaf",
    ...
  ],
  "count": 28
}
```

---

### 3. Predict Disease
```bash
curl -X POST http://localhost:8001/predict \
  -F "file=@leaf_image.jpg"
```
**Response:**
```json
{
  "predicted_class": "Tomato leaf",
  "confidence": 0.92,
  "top_3_predictions": [
    {"class": "Tomato leaf", "confidence": 0.92},
    {"class": "Potato leaf late blight", "confidence": 0.05},
    {"class": "Bell pepper leaf", "confidence": 0.03}
  ]
}
```

---

## 📈 Model Performance

```
Test Accuracy: 58.05%
Test Set: 236 images

Best Performing Classes:
✅ Bell Pepper - 100% accuracy (8/8)
✅ Raspberry - 100% accuracy (7/7)
✅ Strawberry - 100% accuracy (8/8)
✅ Squash Powdery Mildew - 100% accuracy (6/6)

Challenging Classes:
⚠️ Grape - 0% accuracy (0/8)
⚠️ Spider Mites - 0% accuracy (0/12)
⚠️ Corn Gray Spot - 25% accuracy (1/4)
```

---

## 🔧 Step-by-Step Workflow

### 1. First Time Setup
```bash
# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Train model (if not done)
python main.py --train
```

### 2. Daily Usage
```bash
# Run full system
python main.py

# Or start services individually:
python main.py --backend  # Terminal 1
python main.py --frontend # Terminal 2
```

### 3. Check Model Quality
```bash
python main.py --eval
```

### 4. Test Predictions
```bash
# Via API
curl -F "file=@test_image.jpg" http://localhost:8001/predict

# Via Frontend
# Open http://localhost:5174 and upload image
```

---

## 🐛 Troubleshooting

### Model Not Found
```
Error: Model not found at models/model.pt
Solution: python main.py --train
```

### Port Already in Use
```
Address already in use error
Solution: 
  - Kill process: lsof -ti:8001 | xargs kill
  - Or wait a few seconds and retry
```

### Frontend Not Loading
```
Solution: Check if npm is installed
  $ npm --version
  If not: Install Node.js from nodejs.org
```

### Slow Evaluation
```
Model evaluation on CPU is slow (~1-2 min)
Solution: Use GPU if available (CUDA)
```

---

## 📁 File Locations

```
/training/evaluation.py    ← Model evaluation script
/main.py                   ← Main orchestration script
/models/model.pt           ← Trained model (18 MB)
/models/classes.json       ← Class names
/experiment/               ← Jupyter notebooks
```

---

## ✅ Checklist

Before deploying:
- [x] Model trained and saved
- [x] Backend API working
- [x] Frontend UI working  
- [x] Evaluation script running
- [x] Main orchestration working
- [x] 5 Jupyter notebooks created
- [x] Documentation complete

---

## 🎯 Next Steps

1. **Run Full System:**
   ```bash
   python main.py
   ```

2. **Open Browser:**
   ```
   http://localhost:5174
   ```

3. **Upload Leaf Image:**
   - Click "Choose File" or Drag & Drop
   - View instant prediction

4. **Check API:**
   ```
   http://localhost:8001/docs
   ```

5. **Run Evaluation:**
   ```bash
   python main.py --eval
   ```

---

**🌿 System is READY TO USE!** 🚀
