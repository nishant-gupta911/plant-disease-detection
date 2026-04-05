import streamlit as st
import torch
import torch.nn as nn
from PIL import Image
import json
from pathlib import Path
import numpy as np
from torchvision import transforms
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.model import build_model
from backend.config import IMG_SIZE, MODEL_PATH, CLASSES_PATH

# Page config
st.set_page_config(
    page_title="🌱 Plant Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0a1f0d 0%, #1a3a1a 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background: linear-gradient(135deg, #0a1f0d 0%, #1a3a1a 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #7fff00 0%, #6ee600 100%);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #6ee600 0%, #7fff00 100%);
    }
    .metric-card {
        background: rgba(127, 255, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #7fff00;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_and_classes():
    """Load the trained model and class names"""
    try:
        with open(CLASSES_PATH, 'r') as f:
            classes_dict = json.load(f)
            classes = [classes_dict[str(i)] for i in range(len(classes_dict))]

        # Load model
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        model = build_model(num_classes=len(classes), pretrained=False)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model = model.to(device)
        model.eval()

        return model, classes, device
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None, None

def preprocess_image(image, device):
    """Preprocess image for model inference"""
    # Transform
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    img_tensor = transform(image).unsqueeze(0).to(device)
    return img_tensor

def predict(model, image_tensor, classes, device):
    """Make prediction on image"""
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
        # Get top 3 predictions
        top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)
        
        return {
            'predicted_class': classes[predicted.item()],
            'confidence': confidence.item(),
            'top3_classes': [classes[idx] for idx in top3_indices[0]],
            'top3_confidence': top3_probs[0].cpu().numpy()
        }

# Header
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #7fff00; font-size: 3em;'>🌱 Plant Disease Detection</h1>
        <p style='color: #a8d5a8; font-size: 1.2em;'>Identify plant diseases with AI</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📋 About")
    st.markdown("""
    **Plant Disease Detector** uses deep learning to identify plant diseases.
    
    ### Features:
    - 🎯 28 plant disease classes
    - 📷 Real-time image upload
    - 📊 Confidence scores
    - 🔝 Top 3 predictions
    
    ### Model Info:
    - Architecture: ResNet50
    - Image Size: 256x256
    - Device: GPU (MPS/CUDA) or CPU
    """)
    
    st.divider()
    st.markdown("### 📊 Model Stats")
    st.metric("Total Classes", "28", "diseases")
    st.metric("Input Size", "256×256", "pixels")

# Load model
model, classes, device = load_model_and_classes()

if model is None:
    st.error("⚠️ Could not load model. Please ensure the model file exists at: models/model.pt")
else:
    # Main content
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📸 Upload Plant Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image of a plant leaf...",
            type=["jpg", "jpeg", "png", "gif", "bmp"],
            help="Upload a clear image of a plant leaf for disease detection"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="📷 Uploaded Image", use_column_width=True)
            
            # Make prediction
            if st.button("🔍 Analyze Image", key="predict_btn"):
                with st.spinner("🔄 Analyzing image..."):
                    img_tensor = preprocess_image(image, device)
                    prediction = predict(model, img_tensor, classes, device)
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Main prediction
                col_result1, col_result2 = st.columns(2)
                with col_result1:
                    st.metric(
                        "🎯 Predicted Disease",
                        prediction['predicted_class']
                    )
                with col_result2:
                    st.metric(
                        "📊 Confidence",
                        f"{prediction['confidence']*100:.2f}%"
                    )
                
                # Top 3 predictions
                st.subheader("🔝 Top 3 Predictions")
                cols = st.columns(3)
                
                for i, (class_name, confidence) in enumerate(
                    zip(prediction['top3_classes'], prediction['top3_confidence'])
                ):
                    with cols[i]:
                        st.metric(
                            f"#{i+1}",
                            class_name,
                            f"{confidence*100:.2f}%"
                        )
                
                # Confidence chart
                st.subheader("📈 Confidence Distribution")
                chart_data = {
                    'Disease': prediction['top3_classes'],
                    'Confidence': prediction['top3_confidence'] * 100
                }
                st.bar_chart(dict(zip(chart_data['Disease'], chart_data['Confidence'])))
    
    with col2:
        st.subheader("📚 Plant Disease Classes")
        
        # Display all classes
        with st.expander("View all 28 disease classes", expanded=False):
            cols = st.columns(2)
            for i, class_name in enumerate(classes):
                with cols[i % 2]:
                    st.write(f"• {i+1}. {class_name}")
        
        st.divider()
        
        st.subheader("💡 Tips for Best Results")
        st.markdown("""
        - 📷 Use clear, well-lit images
        - 🍃 Focus on diseased leaf areas
        - 🔍 Remove background clutter
        - 📐 Ensure leaf fills most of frame
        - ✂️ Crop to leaf if needed
        """)
        
        st.divider()
        
        st.subheader("ℹ️ Model Information")
        st.markdown(f"""
        - **Model**: ResNet50
        - **Classes**: {len(classes)}
        - **Input Size**: {IMG_SIZE}×{IMG_SIZE}
        - **Device**: {device}
        - **Status**: ✅ Ready
        """)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #7fff00; padding: 20px;'>
        <p>🌿 Plant Disease Detection System | Powered by Deep Learning 🤖</p>
        <p style='font-size: 0.8em;'>© 2026 | All rights reserved</p>
    </div>
""", unsafe_allow_html=True)
