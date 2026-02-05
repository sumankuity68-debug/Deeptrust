import os
import cv2
import numpy as np
import torch
from torchvision import transforms

def extract_frames(video_path, output_folder, max_frames=10):
    """
    Extracts frames from a video and saves them to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    count = 0
    extracted_count = 0
    
    while cap.isOpened() and extracted_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Save every 30th frame (approx 1 per sec if 30fps) for simplicity or just first few
        if count % 30 == 0:
            frame_name = os.path.join(output_folder, f"frame_{extracted_count}.jpg")
            cv2.imwrite(frame_name, frame)
            extracted_count += 1
        count += 1
        
    cap.release()
    print(f"Extracted {extracted_count} frames to {output_folder}")

def preprocess_image(image_path, target_size=(299, 299)):
    """
    Loads an image, resizes it, and normalizes it for the model.
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    
    # Normalize (standard ImageNet normalization)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    img_tensor = transform(img)
    return img_tensor.unsqueeze(0) # Add batch dimension

from glob import glob

def process_dataset(input_dir, output_dir_frames):
    """
    Simulates processing a dataset: Extracts frames from all videos in input_dir.
    """
    video_files = glob(os.path.join(input_dir, "*.mp4")) + glob(os.path.join(input_dir, "*.avi"))
    print(f"Found {len(video_files)} videos in {input_dir}")
    
    for video_path in video_files:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_output_folder = os.path.join(output_dir_frames, video_name)
        print(f"Processing {video_name}...")
        extract_frames(video_path, video_output_folder)

if __name__ == "__main__":
    # Define paths
    DATA_DIR = "data"
    # Assuming structure data/subset/real and data/subset/fake or just flat for now
    # We will look in data/sample_videos
    SAMPLE_VIDEOS = os.path.join(DATA_DIR, "sample_videos")
    PROCESSED_FRAMES = os.path.join(DATA_DIR, "processed_frames")
    
    if os.path.exists(SAMPLE_VIDEOS):
        process_dataset(SAMPLE_VIDEOS, PROCESSED_FRAMES)
        print("Data preprocessing complete.")
    else:
        print(f"Directory {SAMPLE_VIDEOS} not found. Run create_dummy_data.py first.")
