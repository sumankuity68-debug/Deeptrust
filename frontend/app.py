import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DeepTrust - Deepfake Detection",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for "Premium" look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
         transform: scale(1.02);
         box-shadow: 0 0 10px #00f2fe;
    }
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #262730;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ DeepTrust")
st.markdown("### Blockchain-Verified Deepfake Detection System")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.info("Upload your media file (Image or Video) to verify its authenticity.")
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg", "mp4", "avi"])

if uploaded_file is not None:
    with col1:
        # Display Preview
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        else:
            st.video(uploaded_file)
            
    with col2:
        st.subheader("Analysis Results")
        if st.button("🔍 Verify Authenticity"):
            with st.spinner("Processing with AI & Blockchain..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/verify/", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        label = data.get("label", "Unknown")
                        conf = data.get("confidence", "0%")
                        tx_hash = data.get("blockchain_tx", "N/A")
                        file_hash = data.get("hash", "N/A")
                        
                        # Display
                        if label == "Real":
                            st.success(f"### Result: {label}")
                        else:
                            st.error(f"### Result: {label}")
                            
                        st.metric("Confidence Score", conf)
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <h4>🔗 Blockchain Verification</h4>
                            <p><b>Media Hash (SHA-256):</b> <code style='font-size:0.8em'>{file_hash}</code></p>
                            <p><b>Transaction ID (Polygon):</b> <code style='font-size:0.8em'>{tx_hash}</code></p>
                            <p><i>Immutable record stored on decentralized ledger.</i></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
                    st.warning("Make sure the FastAPI backend is running on port 8000.")

st.markdown("---")
st.caption("DeepTrust System v1.0 | Powered by XceptionNet/EfficientNet & Polygon")
