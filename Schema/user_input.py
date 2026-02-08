from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated 
from config.city_tier import tier_1_cities, tier_2_cities

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
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, value:str) -> str:
        return value.strip().title()  
        