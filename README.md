# DeepTrust: AI & Blockchain Deepfake Detection

DeepTrust is a full-stack system that detects deepfakes using State-of-the-Art AI (EfficientNet/ResNet) and anchors verification results on the Polygon blockchain for immutability.

## Project Structure
- `backend/`: FastAPI backend for model inference and hashing.
- `frontend/`: Streamlit dashboard for user interaction.
- `models/`: AI model definition (DeepTrustModel).
- `contracts/`: Solidity smart contracts for Polygon integration.
- `scripts/`: Utility scripts for data processing and hashing.
- `data/`: Data storage (placeholder).

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Update `.env` with your Blockchain credentials (RPC, Private Key, Contract Address).

3. **Run System (Merged)**:
   ```bash
   python run_system.py
   ```
   This script launches both the backend and frontend simultaneously.	

   OR Run Individually:
   - Backend: `uvicorn backend.main:app --reload --port 8000`
   - Frontend: `streamlit run frontend/app.py`

## Blockchain Note
The Smart Contract is located in `contracts/DeepTrust.sol`. To verify on-chain, deploy this contract to Polygon Mumbai Testnet and update the backend with the contract address and ABI.

## Model
The system defaults to `EfficientNet` (if available) or `ResNet50`. It predicts a "Real" or "Fake" label and a confidence score.
