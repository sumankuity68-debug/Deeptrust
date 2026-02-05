import subprocess
import time
import os
import sys

def run_system():
    print("🚀 Starting DeepTrust System...")
    
    # Define paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKEND_CMD = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    FRONTEND_CMD = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"]
    
    print(f"📂 Project Root: {BASE_DIR}")
    
    try:
        # Start Backend
        print("🔌 Launching Backend (FastAPI)...")
        backend_process = subprocess.Popen(BACKEND_CMD, cwd=BASE_DIR)
        
        # Wait a moment for backend to initialize
        time.sleep(5)
        
        # Start Frontend
        print("🖥️ Launching Frontend (Streamlit)...")
        frontend_process = subprocess.Popen(FRONTEND_CMD, cwd=BASE_DIR)
        
        print("\n✅ System Running!")
        print("   👉 Backend: http://localhost:8000/docs")
        print("   👉 Frontend: http://localhost:8501")
        print("\nPress Ctrl+C to stop both servers.")
        
        # Keep main script alive
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ System stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'backend_process' in locals(): backend_process.terminate()
        if 'frontend_process' in locals(): frontend_process.terminate()

if __name__ == "__main__":
    run_system()
