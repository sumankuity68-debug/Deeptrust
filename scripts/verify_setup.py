import torch
import sys
import os

def check_gpu():
    print("Checking GPU availability...")
    if torch.cuda.is_available():
        print(f"[OK] GPU is available: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("[WARN] GPU is NOT available. Using CPU.")
        return False

def check_requirements():
    print("\nChecking key libraries...")
    try:
        import cv2
        print(f"[OK] OpenCV version: {cv2.__version__}")
        import fastapi
        print(f"[OK] FastAPI version: {fastapi.__version__}")
        import web3
        print(f"[OK] Web3 version: {web3.__version__}")
    except ImportError as e:
        print(f"[ERR] Missing library: {e}")

if __name__ == "__main__":
    check_gpu()
    check_requirements()
    print("\nEnvironment verification complete.")
