from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated 
import pickle
import pandas as pd

# importing the ml model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

# tier of the cities
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
# pydantic model to validate the incoming data
class UserInput(BaseModel): 
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119", example=30)]
    weight: Annotated[float, Field(..., gt=0, description="Weight must be a positive number", example=70.5)]
    height: Annotated[float, Field(..., gt=0, description="Height must be a positive number", example=175.2)]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income in lakhs per annum must be a positive number", example=10.0)]
    smoker: Annotated[bool, Field(..., description="Whether the person is a smoker or not", example=False)]
    city: Annotated[str, Field(..., description="City of residence", example="Mumbai")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the person", example="private_job")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height / 100) ** 2)  # height converted to meters
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif 25 <= self.age < 45:
            return 'adult'
        elif 45 <= self.age < 60:
            return 'middle_aged'
        else:
            return 'senior'
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        

@app.post("/predict")
def predict_premium(data:UserInput):
    input_df= pd.DataFrame([{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])
    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code = 200, content={'predicted_category':prediction})
