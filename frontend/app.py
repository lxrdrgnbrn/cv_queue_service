import streamlit as st
import requests
import os
import time

API_URL = API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("CV Service")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Original Image", use_container_width=True)

    if st.button("Detect Objects"):
        with st.spinner("Uploading and Processing..."):
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                response.raise_for_status()
                data = response.json()
                
                task_id = data.get("task_id")
                st.success(f"Task created! ID: {task_id}")
                
                filename = os.path.basename(data["input_path"])
                result_path = os.path.join("data", "results", filename)
                
                st.info("Waiting for worker...")
                
                for _ in range(10):
                    if os.path.exists(result_path):
                        st.image(result_path, caption="Processed Image", use_container_width=True)
                        break
                    time.sleep(1)
                else:
                    st.error("Timeout: Worker didn't finish in time.")
                    
            except Exception as e:
                st.error(f"Error: {e}")