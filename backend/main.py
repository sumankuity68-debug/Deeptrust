from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add project root to sys.path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import get_model
from scripts.hashing import generate_file_hash, generate_bytes_hash
from scripts.preprocessing import preprocess_image
import torch

app = FastAPI(title="DeepTrust Backend", description="API for Deepfake Detection and Blockchain Verification")

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Load Model globally
try:
    model = get_model()
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

@app.get("/")
def read_root():
    return {"message": "Welcome to DeepTrust Backend. Use /verify/ to check media."}

@app.post("/verify/")
async def verify_media(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded.")
        
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save file
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        
    # 1. Generate Hash
    file_hash = generate_file_hash(file_location)
    
    # 2. Run AI Model (Assuming image for now, video needs frame extraction logic)
    # For simplification in this step, we pretend it's an image or we process first frame
    try:
        # Check extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png']:
            img_tensor = preprocess_image(file_location)
            score = model.predict(img_tensor)
        elif ext in ['.mp4', '.avi', '.mov']:
            # TODO: thorough video analysis
            # For now, just return a dummy score or implement frame extraction if time permits
            # Let's say we analyze the first frame or a middle frame
            import cv2
            cap = cv2.VideoCapture(file_location)
            ret, frame = cap.read()
            cap.release()
            if ret:
                # Need to convert CV2 frame (BGR) to PIL/Tensor style expected by preprocess
                # But preprocess_image takes a path. Let's send a temp frame path.
                temp_frame = os.path.join(UPLOAD_DIR, "temp_frame.jpg")
                cv2.imwrite(temp_frame, frame)
                img_tensor = preprocess_image(temp_frame)
                score = model.predict(img_tensor)
            else:
                score = 0.5 # Uncertain
        else:
             raise HTTPException(status_code=400, detail="Unsupported file format")
             
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")
    
    # Interpretation: 0=Real, 1=Fake (based on typical binary formatting, user said 'authenticity score')
    # Let's assume model output 1.0 is FAKE and 0.0 is REAL.
    label = "Fake" if score > 0.5 else "Real"
    confidence = score * 100 if label == "Fake" else (1 - score) * 100
    
    # 3. Blockchain Interaction
    tx_hash = "N/A - Blockchain Config Missing"
    
    # Check if Blockchain env vars are set (Mocking the real flow)
    # In a real scenario, you would load these from .env
    RPC_URL = os.getenv("RPC_URL", "") # e.g. Polygon RPC
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
    
    if RPC_URL and PRIVATE_KEY and CONTRACT_ADDRESS:
        try:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(RPC_URL))
            if w3.is_connected():
                # Simplified ABI for recordMedia function
                contract_abi = [
                    {
                        "inputs": [
                            {"internalType": "string", "name": "_mediaHash", "type": "string"},
                            {"internalType": "uint256", "name": "_score", "type": "uint256"}
                        ],
                        "name": "recordMedia",
                        "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    }
                ]
                
                contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
                
                # Build Transaction
                account = w3.eth.account.from_key(PRIVATE_KEY)
                score_int = int(score * 100) # Convert 0.98 to 98
                
                nonce = w3.eth.get_transaction_count(account.address)
                tx = contract.functions.recordMedia(file_hash, score_int).build_transaction({
                    'chainId': 80001, # Mumbai Testnet ID (example)
                    'gas': 200000,
                    'gasPrice': w3.to_wei('50', 'gwei'),
                    'nonce': nonce,
                })
                
                # Sign and Send
                signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
                tx_hash_bytes = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_hash = w3.to_hex(tx_hash_bytes)
                print(f"✅ Transaction sent: {tx_hash}")
            else:
                print("❌ Blockchain connection failed")
        except Exception as e:
            print(f"❌ Blockchain interaction error: {e}")
            tx_hash = f"Error: {str(e)}"
    
    return {
        "filename": file.filename,
        "hash": file_hash,
        "score_raw": score,
        "label": label,
        "confidence": f"{confidence:.2f}%",
        "blockchain_tx": tx_hash,
        "message": "Verification successful"
    }
