# FastAPI Insurance Premium Category Predictor

## Project Intent
This project is primarily a **FastAPI learning project**.

The goal is to understand and practice end-to-end API development principles such as:
- request validation with Pydantic
- feature engineering inside API logic
- serving a trained ML pipeline through REST endpoints
- integrating a frontend client with the API

The core idea here is **not** to build the most optimal ML model, but to strengthen practical FastAPI skills.

## What I Built (End-to-End)
I built a complete workflow from model training to user-facing prediction:
1. Trained a classification pipeline in `ML_Model_Building.ipynb`.
2. Saved the trained model as `model.pkl`.
3. Exposed prediction via FastAPI endpoint (`/predict`) in `app.py`.
4. Built a simple Streamlit frontend in `front_end.py` to consume the API.

## Tech Stack
- **Backend API:** FastAPI
- **Data validation & schema modeling:** Pydantic (v2 style, including `@computed_field`)
- **ML/Data processing:** scikit-learn, pandas
- **Model serialization:** pickle
- **Frontend/UI:** Streamlit
- **API client from UI:** requests
- **Language:** Python

## Project Structure
```text
FastAPI_implemntation/
├── app.py                    # FastAPI app for premium prediction
├── front_end.py              # Streamlit app (calls FastAPI /predict)
├── ML_Model_Building.ipynb   # Training and pipeline export workflow
├── model.pkl                 # Serialized trained model pipeline
├── Data/
│   └── insurance.csv         # Source dataset
└── .gitignore
```

## Prediction API Design
### Endpoint
- `POST /predict`

### Input fields
- `age` (int)
- `weight` (float)
- `height` (float)
- `income_lpa` (float)
- `smoker` (bool)
- `city` (str)
- `occupation` (enum: `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`)

### Derived features inside API
The API computes these features before inference:
- `bmi`
- `lifestyle_risk`
- `age_group`
- `city_tier`

### Response
```json
{
  "predicted_category": "<class_label>"
}
```

## How to Run Locally
### 1. Go to project folder
```bash
cd /Users/rohan/Desktop/FastAPI/FastAPI_implemntation
```

### 2. Install dependencies
```bash
pip install fastapi "uvicorn[standard]" pydantic pandas scikit-learn streamlit requests jupyter
```

### 3. Start FastAPI server
```bash
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```

### 4. Start Streamlit frontend (new terminal)
```bash
streamlit run front_end.py
```

### 5. Open docs and app
- FastAPI Swagger: `http://127.0.0.1:8002/docs`
- Streamlit UI: shown in terminal after running Streamlit

## Example API Request
```bash
curl -X POST "http://127.0.0.1:8002/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 70,
    "height": 175,
    "income_lpa": 10,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'
```

## Key FastAPI Learnings Captured in This Project
- Structuring a production-style inference endpoint
- Enforcing clean input contracts with Pydantic
- Using computed fields for reusable business logic
- Returning explicit JSON responses
- Connecting backend and frontend in a simple full-stack ML app

## Notes for Future Improvements
- Add `requirements.txt` and version pinning for reproducibility.
- Add automated tests for `/predict` input/output behavior.
- Containerize with Docker for simpler deployment.
- Add better model tracking and evaluation reporting.

## Author Note
This repository documents my hands-on journey in learning FastAPI through a real ML-serving use case.
