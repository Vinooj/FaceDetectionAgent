"""Streamlit UI for Face Detection and Identification Application."""
print("Executing app.py")

import asyncio
import tempfile
from pathlib import Path
import streamlit as st
from PIL import Image
import cv2
import numpy as np
from fastmcp import Client


# Page configuration
print("Configuring Streamlit page")
st.set_page_config(
    page_title="Face Detection & Identification",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .status-success {
        color: #4CAF50;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #e8f5e9;
    }
    .status-failure {
        color: #f44336;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffebee;
    }
    .header { color: #333; }
    </style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        """
        This application detects faces in an uploaded image and verifies if those 
        same individuals appear in a webcam capture using AI-powered face identification.
        """
    )
    
    st.header("How to Use")
    st.write(
        """
        1. Upload an image containing faces
        2. Capture an image from your webcam
        3. Click "Run Identification" to match faces
        4. View identification results
        """
    )


# Main content
st.title("👤 Face Detection and Identification")
print("Initializing session state")
# Initialize session state
if "uploaded_image_path" not in st.session_state:
    st.session_state.uploaded_image_path = None
if "webcam_image_path" not in st.session_state:
    st.session_state.webcam_image_path = None
if "detection_results" not in st.session_state:
    st.session_state.detection_results = None


# Initialize FastMCP client
@st.cache_resource
def get_mcp_client():
    """Get or create FastMCP client."""
    print("Attempting to get FastMCP client")
    try:
        return Client("http://localhost:8000")
    except Exception as e:
        st.error(f"Failed to connect to MCP server: {str(e)}")
        return None


# Two-column layout
col1, col2 = st.columns(2)

# Column 1: Upload Image
with col1:
    st.subheader("📤 Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose an image (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        key="image_uploader"
    )
    
    if uploaded_file:
        print("Image uploaded")
        # Save uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.getbuffer())
            st.session_state.uploaded_image_path = tmp.name
        
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)


# Column 2: Webcam Capture
with col2:
    st.subheader("📷 Capture from Webcam")
    
    if st.button("📹 Activate Camera", key="camera_btn"):
        st.session_state.camera_active = True
    
    if st.session_state.get("camera_active", False):
        print("Camera activated")
        client = get_mcp_client()
        if client:
            with st.spinner("Starting camera..."):
                # Create a temporary file to save the captured image
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    st.session_state.webcam_image_path = tmp.name

                # Call the capture_image tool
                print(f"Calling capture_image tool {st.session_state.webcam_image_path}")
                result = asyncio.run(client.call_tool("capture_image", file_path=st.session_state.webcam_image_path))
                print(f"Result - {result}")

                if result and result.get("success"):
                    print("Image captured successfully")
                    # Display the captured image
                    image = Image.open(st.session_state.webcam_image_path)
                    st.image(image, caption="Captured Image", use_column_width=True)
                    
                    if st.button("🔄 Retake Picture"):
                        st.session_state.camera_active = False
                        st.rerun()
                else:
                    st.error(f"❌ Unable to access webcam: {result.get('error')}")
        else:
            st.error("❌ Could not connect to MCP server. Ensure it's running on http://localhost:8000")


# Run Identification Section
st.divider()
col_run, col_status = st.columns([2, 3])

with col_run:
    run_identification = st.button(
        "🚀 Run Identification",
        key="run_identification",
        use_container_width=True
    )

# Identification Status Display
with col_status:
    st.subheader("📊 Identification Status")


if run_identification:
    print("Run Identification button clicked")
    if not st.session_state.uploaded_image_path or not st.session_state.webcam_image_path:
        st.error("⚠️ Please upload an image and capture a webcam image first.")
    else:
        try:
            client = get_mcp_client()
            
            if client is None:
                st.error("❌ Could not connect to MCP server. Ensure it's running on http://localhost:8000")
            else:
                with st.spinner("🔍 Detecting faces..."):
                    # Call detect_faces tool
                    print("Calling detect_faces tool")
                    detection_result = asyncio.run(client.call_tool(
                        "detect_faces",
                        image_path=st.session_state.uploaded_image_path
                    ))
                    
                    if not detection_result.get("success"):
                        st.error(f"❌ Face detection failed: {detection_result.get('error')}")
                    else:
                        faces = detection_result.get("faces", [])
                        st.session_state.detection_results = faces
                        
                        if not faces:
                            st.warning("⚠️ No faces detected in the uploaded image.")
                        else:
                            st.success(f"✅ Detected {len(faces)} face(s)")
                            
                            # Process each detected face
                            identification_results = []
                            
                            for idx, face in enumerate(faces):
                                st.divider()
                                st.write(f"**Face {idx + 1}**")
                                
                                # Extract face bounding box
                                bbox = face.get("bbox", [])
                                if bbox:
                                    x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                                    
                                    # Crop face from image
                                    original_img = cv2.imread(st.session_state.uploaded_image_path)
                                    if original_img is not None:
                                        cropped_face = original_img[y1:y2, x1:x2]
                                        
                                        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                                            cv2.imwrite(tmp.name, cropped_face)
                                            cropped_path = tmp.name
                                        
                                        # Display cropped face
                                        cropped_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
                                        col_face, col_result = st.columns([1, 2])
                                        
                                        with col_face:
                                            st.image(cropped_rgb, caption=f"Face {idx + 1}", use_column_width=True)
                                        
                                        with col_result:
                                            with st.spinner(f"🔎 Identifying face {idx + 1}..."):
                                                # Call identify_face tool
                                                print(f"Calling identify_face tool for face {idx + 1}")
                                                identify_result = asyncio.run(client.call_tool(
                                                    "identify_face",
                                                    base_image_path=cropped_path,
                                                    image_to_search_path=st.session_state.webcam_image_path
                                                ))
                                                
                                                if identify_result.get("success"):
                                                    is_match = identify_result.get("is_match")
                                                    identification_results.append({
                                                        "face_id": idx + 1,
                                                        "match": is_match
                                                    })
                                                    
                                                    if is_match:
                                                        st.markdown(
                                                            '<p class="status-success">✅ MATCH FOUND</p>',
                                                            unsafe_allow_html=True
                                                        )
                                                    else:
                                                        st.markdown(
                                                            '<p class="status-failure">❌ NO MATCH</p>',
                                                            unsafe_allow_html=True
                                                        )
                                                else:
                                                    st.error(f"❌ Identification failed: {identify_result.get('error')}")
        
        except Exception as e:
            st.error(f"❌ Error during identification: {str(e)}")
