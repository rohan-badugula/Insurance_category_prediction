# Insurance Premium Category Prediction API

## Overview
This is a learning-focused end-to-end project that serves an ML model through FastAPI and consumes it from a Streamlit UI.

The project demonstrates:
- schema validation with Pydantic
- runtime feature engineering inside the API layer
- model loading and inference with scikit-learn
- frontend integration with a REST endpoint

## Project Goals
- Practice building a clean FastAPI inference service.
- Learn how to convert raw user input into model-ready features.
- Build a simple full-stack workflow: API + UI + trained model artifact.

## Current Architecture
1. User enters details in Streamlit (`front_end.py`).
2. Streamlit sends a `POST` request to `/predict`.
3. FastAPI validates request body using `UserInput` schema.
4. Derived features are computed (`bmi`, `age_group`, `lifestyle_risk`, `city_tier`).
5. Model inference runs via `Model/predict.py`.
6. API returns `predicted_category` as JSON.

## Repository Structure
```text
Insurance_Premium_Project/
├── app.py                    # FastAPI app with routes and prediction orchestration
├── front_end.py              # Streamlit client application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── ML_Model_Building.ipynb   # Model training/export notebook
├── Data/
│   └── insurance.csv         # Training dataset
├── Model/
│   ├── model.pkl             # Serialized scikit-learn pipeline
│   └── predict.py            # Model loading + predict_output()
├── Schema/
│   └── user_input.py         # Pydantic input schema and computed features
└── config/
    └── city_tier.py          # Tier-1 and Tier-2 city lists
```

## API Endpoints
### `GET /`
Basic welcome message to confirm the server is reachable.

### `GET /health`
Health endpoint returning API status and model version.

Example response:
```json
{
  "status": "API is healthy and running.",
  "version": "1.0.0"
}
```

### `POST /predict`
Accepts user profile details and returns insurance premium category prediction.

## Input Contract (`POST /predict`)
Fields:
- `age` (`int`): must be between `1` and `119`
- `weight` (`float`): in kilograms, must be `> 0`
- `height` (`float`): in meters, expected range `0.5` to `2.5`
- `income_lpa` (`float`): income in lakhs per annum, must be `> 0`
- `smoker` (`bool`)
- `city` (`str`)
- `occupation` (`str` enum): `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`

Derived fields computed inside API schema:
- `bmi = weight / (height^2)`
- `age_group` based on age bucket
- `lifestyle_risk` based on smoker status and BMI
- `city_tier` based on configured city lists

## Example Request
```bash
curl -X POST "http://127.0.0.1:8002/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 70,
    "height": 1.75,
    "income_lpa": 10,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'
```

## Example Success Response
```json
{
  "predicted_category": "Low"
}
```

## Local Setup
### 1. Move to project directory
```bash
cd /Users/rohan/Desktop/FastAPI/Insurance_Premium_Project
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run FastAPI server
```bash
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```

### 5. Run Streamlit UI (new terminal, same venv)
```bash
streamlit run front_end.py
```

### 6. Open applications
- FastAPI docs: `http://127.0.0.1:8002/docs`
- Streamlit app: URL shown in Streamlit terminal output

## Development Notes
- Model file is loaded at import time from `Model/model.pkl`.
- Prediction helper expects a dictionary with model feature names.
- City input is normalized using `.strip().title()` before tier mapping.
- Height is handled in meters across schema, API examples, and frontend.

## Learning Outcomes
This project is a solid practice baseline for:
- FastAPI routing and response handling
- Pydantic v2 schema design with computed fields
- API-side feature engineering
- Serving serialized ML models
- Connecting UI and backend in a simple production-style flow
