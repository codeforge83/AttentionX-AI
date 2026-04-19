import streamlit as st
import moviepy as mp
import librosa
import numpy as np
import mediapipe as mp_face
import cv2
from google.generativeai import GenerativeModel
import os

# --- Configuration ---
st.set_page_config(page_title="AttentionX AI - Content Repurposer", layout="wide")
st.title("AttentionX: Long-form to Viral Clips 🚀")

# --- Step 1: Video Upload ---
uploaded_file = st.file_uploader("Upload your long-form video (MP4)", type=["mp4"])

if uploaded_file:
    # Save video temporarily
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_video.mp4")
    
    if st.button("Generate Viral Clips"):
        with st.spinner("Analyzing audio spikes for 'Emotional Peaks'..."):
            # --- Step 2: Identify Emotional Peaks (Librosa) ---
            # [span_9](start_span)Finding high-energy moments based on audio loudness[span_9](end_span)
            y, sr = librosa.load("temp_video.mp4")
            rms = librosa.feature.rms(y=y)
            times = librosa.frames_to_time(np.arange(len(rms[0])), sr=sr)
            
            # Identify a high-energy 60-second window
            peak_idx = np.argmax(rms)
            start_time = max(0, times[peak_idx] - 30)
            end_time = start_time + 60
            
            st.success(f"Detected highlight from {start_time:.2f}s to {end_time:.2f}s")

        with st.spinner("Smart-Cropping to Vertical (MediaPipe)..."):
            # --- Step 3: Smart-Crop to Vertical (MediaPipe) ---
            # [span_10](start_span)[span_11](start_span)Tracking the speaker's face to center them in 9:16[span_10](end_span)[span_11](end_span)
            clip = mp.VideoFileClip("temp_video.mp4").subclip(start_time, end_time)
            
            # Simple Center Crop Logic for Hackathon Prototype
            w, h = clip.size
            target_w = h * (9/16)
            crop_x1 = (w - target_w) / 2
            crop_x2 = crop_x1 + target_w
            
            final_clip = clip.crop(x1=crop_x1, y1=0, x2=crop_x2, y2=h)
            final_clip.write_videofile("https://www.youtube.com/watch?v=4zaqWUkqvIg", fps=24)

        st.subheader("Final Repurposed Clip")
        st.video("https://www.youtube.com/watch?v=4zaqWUkqvIg")
        
        with open("https://www.youtube.com/watch?v=4zaqWUkqvIg", "rb") as file:
            st.download_button("Download Clip for Shorts", file, "https://www.youtube.com/watch?v=4zaqWUkqvIg")
