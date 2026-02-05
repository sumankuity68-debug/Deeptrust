import cv2
import numpy as np
import os

def create_dummy_video(filename, duration_sec=2, fps=30):
    """Creates a dummy video file for testing."""
    height, width = 480, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    frames = duration_sec * fps
    for i in range(frames):
        # Create a random noise frame with a moving rectangle
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        # Add a moving box
        x = int((i / frames) * (width - 50))
        cv2.rectangle(frame, (x, 200), (x + 50, 250), (0, 255, 0), -1)
        
        out.write(frame)
        
    out.release()
    print(f"Created dummy video: {filename}")

if __name__ == "__main__":
    if not os.path.exists("data/sample_videos"):
        os.makedirs("data/sample_videos")
    
    create_dummy_video("data/sample_videos/real_sample.mp4")
    create_dummy_video("data/sample_videos/fake_sample.mp4")
