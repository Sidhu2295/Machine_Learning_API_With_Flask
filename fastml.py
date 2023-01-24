from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import sklearn
import pandas as pd
import pickle
import json

app = FastAPI()

class information(BaseModel):
    location: str
    total_sqft: float
    bath: float
    bhk: int

with open('banglore_home_prices_model.pickle', 'rb') as f:
    model = pickle.load(f)
    print('Model is downloaded...')

with open('columns.json','r') as f:
    data_columns = json.load(f)['data_columns']
    print('Data columns are downloaded...')

@app.post('/')
async def predict_price(data:information):
    data = data.dict()
    location = data['location']
    sqft = data['total_sqft']
    bath = data['bath']
    bhk = data['bhk']
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index]=1

    return model.predict([x])[0]

if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
