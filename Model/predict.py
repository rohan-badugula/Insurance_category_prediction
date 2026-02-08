import pickle
import pandas as pd

# importing the ml model
with open("Model/model.pkl", "rb") as f:
    model = pickle.load(f)

# sample model version number, can be used for future reference
model_version = "1.0.0"


def predict_output(user_input: dict):
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]
    return prediction