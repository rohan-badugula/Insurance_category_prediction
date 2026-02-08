from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Schema.user_input import UserInput
from Model.predict import predict_output, model_version


app = FastAPI()

# this is human redable endpoint to check if the api is working fine or not
@app.get("/")
def home():
    return {'message': 'Welcome to the Insurance Premium Prediction API. Use the /predict endpoint to get predictions.'}


# this is for AWS or kubernetest to autopmatically check the health of API. 
@app.get("/health")
def health_check():
    return {'status': 'API is healthy and running.', 'version': model_version}


@app.post("/predict")
def predict_premium(data:UserInput):
    input_data= {
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    try:
        prediction = predict_output(input_data)
        return JSONResponse(status_code = 200, content={'predicted_category':prediction})
    except Exception as e:
        return JSONResponse(status_code = 500, content={'error': str(e)})