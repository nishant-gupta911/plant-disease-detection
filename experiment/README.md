# 📊 Plant Disease Detection Lab - Jupyter Notebooks

## ✅ PROJECT COMPLETION STATUS

All 5 Jupyter Notebooks have been successfully created, executed, and saved with outputs.

**Location:** `/Users/nishant/Documents/vscode/plant_disease_detection/experiment/`

---

## 📋 NOTEBOOKS SUMMARY

### 1️⃣ **Experiment 1: Dataset Analysis** ✓
- **File:** `experiment_1.ipynb`
- **Status:** ✅ Executed Successfully
- **Duration:** 13ms
- **Output:** Dataset statistics (class count, image count)

**Content:**
- Reads dataset using `os.listdir()`
- Counts 28 disease classes
- Counts 2,336 total training images
- Displays class names and statistics

---

### 2️⃣ **Experiment 2: Data Preprocessing** ✓
- **File:** `experiment_2.ipynb`
- **Status:** ✅ Executed Successfully
- **Duration:** 3.6 seconds
- **Output:** Transform pipeline demonstration

**Content:**
- Defines torchvision transforms pipeline
- Resizes images to 224x224
- Applies ImageNet normalization
- Tests on sample image with properties output

---

### 3️⃣ **Experiment 3: Class Distribution Analysis** ✓
- **File:** `experiment_3.ipynb`
- **Status:** ✅ Executed Successfully
- **Duration:** 2.7 seconds
- **Outputs:** 
  - ✅ Class distribution table (DataFrame)
  - ✅ Bar chart visualization
  - ✅ Pie chart (percentage distribution)
  - 📁 File saved: `exp3_distribution.png`

**Content:**
- Creates pandas DataFrame with class counts
- Sorts by image count
- Visualizes 2 charts (bar + pie)
- Statistics: 28 classes, 2,336 images

---

### 4️⃣ **Experiment 4: Healthy vs Diseased** ✓
- **File:** `experiment_4.ipynb`
- **Status:** ✅ Executed Successfully
- **Duration:** 1.6 seconds
- **Outputs:**
  - ✅ Classification results table
  - ✅ Bar charts (2 comparisons)
  - 📁 File saved: `exp4_healthy_diseased.png`

**Content:**
- Categorizes classes: "Healthy" vs "Diseased"
- Results: 0 Healthy, 28 Diseased classes
- Total: 2,336 diseased images (100%)
- Comparison visualization with counts

---

### 5️⃣ **Experiment 5: Top Disease Classes** ✓
- **File:** `experiment_5.ipynb`
- **Status:** ✅ Executed Successfully
- **Duration:** 1.7 seconds
- **Outputs:**
  - ✅ Top 10 ranked table
  - ✅ Horizontal bar chart
  - ✅ Pie chart (percentage)
  - 📁 File saved: `exp5_top_classes.png`

**Content:**
- Top 10 diseases by image count
- Corn leaf blight leads (179 images, 7.7%)
- Top 10 covers 59.8% of total images
- Full ranking with percentages

---

## 📸 SCREENSHOT INSTRUCTIONS FOR LAB SUBMISSION

### **Experiment 1: Dataset Analysis**

**Screenshot 1 - Code Output:**
1. Open `experiment_1.ipynb`
2. Scroll down to see the executed cell output
3. Expected output shows:
   - `✓ Dataset found at: ...`
   - Total Classes: 28
   - Class name list with image counts per class
4. **Take screenshot** of this output

**Screenshot 2 - Dataset Structure:**
1. In terminal, run: `ls -la data/PlantDoc-Dataset-master/train/`
2. Shows all 28 disease class folders
3. **Take screenshot** of directory listing

**Screenshot 3 - Notebook Summary:**
1. Look at the notebook execution indicator
2. Cell execution order visible
3. **Take screenshot** showing notebook is executed (✓ checkmark)

---

### **Experiment 2: Data Preprocessing**

**Screenshot 1 - Transform Pipeline Output:**
1. Open `experiment_2.ipynb`
2. Scroll to see cell output showing:
   - Transform pipeline definition with all steps
   - Image properties: Size, Mode, Shape, Data Type
   - Min/Max/Mean/Std values
3. **Take screenshot** of console output

**Screenshot 2 - Code Cell:**
1. Show the code cell with torchvision imports
2. Visible: `transforms.Compose()`, `transforms.Resize()`, `transforms.ToTensor()`
3. **Take screenshot** of code

**Screenshot 3 - Output Summary:**
1. Show the final output:
   - "✓ Preprocessing pipeline defined and tested successfully!"
   - Image transformation properties
2. **Take screenshot**

---

### **Experiment 3: Class Distribution Analysis**

**Screenshot 1 - Statistical Output:**
1. Open `experiment_3.ipynb`
2. Scroll to see table and statistics:
   - CLASS DISTRIBUTION TABLE
   - Total Classes: 28
   - Total Images: 2,336
   - Mean Images/Class: 83.43
   - Statistical measures
3. **Take screenshot** of this table

**Screenshot 2 - Bar Chart:**
1. See the bar chart displaying all 28 classes
2. X-axis: Disease classes (C1-C28)
3. Y-axis: Number of images
4. Title: "Plant Disease Class Distribution"
5. **Take screenshot** of the bar chart

**Screenshot 3 - Pie Chart:**
1. Immediately below bar chart
2. Shows percentage distribution
3. Title: "Class Distribution (Percentage)"
4. **Take screenshot** of pie chart

---

### **Experiment 4: Healthy vs Diseased Analysis**

**Screenshot 1 - Classification Results:**
1. Open `experiment_4.ipynb`
2. Scroll to see output:
   - CLASSIFICATION RESULTS table
   - Each class labeled as "Healthy" or "Diseased"
   - Image counts per class
3. **Take screenshot** of table

**Screenshot 2 - Summary Statistics:**
1. Same cell, scroll down to see:
   - Healthy Classes: 0
   - Diseased Classes: 28
   - Healthy Images: 0
   - Diseased Images: 2,336
   - Percentages: Healthy 0.00%, Diseased 100.00%
3. **Take screenshot** of statistics

**Screenshot 3 - Comparison Charts:**
1. See two side-by-side bar charts
2. Left: "Disease Classes Distribution" (class count)
3. Right: "Training Images Distribution" (image count)
4. **Take screenshot** of both charts

---

### **Experiment 5: Top Disease Classes**

**Screenshot 1 - Top 10 Rankings:**
1. Open `experiment_5.ipynb`
2. Scroll to see table:
   - Rank 1-10 diseases
   - Disease Class names
   - Image Count
   - Percentage
3. **Take screenshot** of ranking table

**Screenshot 2 - Bar Chart:**
1. See horizontal bar chart
2. Shows top 10 by image count
3. Each bar labeled with disease name and percentage
4. Title: "Top 10 Disease Classes by Image Count"
5. **Take screenshot** of bar chart

**Screenshot 3 - Pie Chart:**
1. Right side: Pie chart with percentages
2. Numbered #1-#10
3. Title: "Top 10 Classes: Percentage of Total Images"
4. **Take screenshot** of pie chart

---

## 📁 GENERATED FILES

```
experiment/
├── experiment_1.ipynb          ✅ Executed
├── experiment_2.ipynb          ✅ Executed
├── experiment_3.ipynb          ✅ Executed
├── exp3_distribution.png       ✅ Chart output
├── experiment_4.ipynb          ✅ Executed
├── exp4_healthy_diseased.png   ✅ Chart output
├── experiment_5.ipynb          ✅ Executed
└── exp5_top_classes.png        ✅ Chart output
```

---

## ✨ KEY FINDINGS

| Metric | Value |
|--------|-------|
| Total Disease Classes | 28 |
| Total Training Images | 2,336 |
| Avg Images/Class | 83.43 |
| Most Common Disease | Corn leaf blight (179) |
| Healthy Classes | 0 |
| Diseased Classes | 28 |
| Top 10 Coverage | 59.8% |
| Dataset Balance | Moderate imbalance |

---

## 🚀 RUNNING THE NOTEBOOKS

To run any notebook:

```bash
cd /Users/nishant/Documents/vscode/plant_disease_detection/experiment

# In VS Code:
1. Open the notebook file
2. Press Ctrl+Shift+Alt+Enter (or Cmd+Shift+Alt+Enter on Mac)
3. Or click "Run All" button in notebook toolbar
```

---

## ✅ EXECUTION CONFIRMATION

All notebooks:
- ✅ Successfully created
- ✅ Successfully executed
- ✅ Outputs visible and saved
- ✅ No errors encountered
- ✅ Ready for submission

---

**Created:** March 20, 2026
**Dataset:** PlantDoc-Dataset-master (Folder-based, 28 classes)
**Libraries Used:** os, pandas, matplotlib, torchvision
**Status:** Complete & Tested ✓
