from fastapi import FastAPI
import pickle
from pydantic import BaseModel

rf_model = pickle.load(open('rf_model.pkl','rb'))

app=FastAPI()


@app.get('/')
async def root():
    return {'message':'Hello World!'}

with open('rf_model.pkl','rb') as f:
    rf_model=pickle.load(f)

class PassengerModel(BaseModel):
    sex: int
    age: int
    embarked: str
    p_class: int

@app.post('/')
async def predict_survival(passenger_data: PassengerModel):
    passenger_array=[]
    if passenger_data.sex=='female':
        passenger_array.append(0)
    else:
        passenger_array.append(1)
    passenger_array.append(passenger_data.age)
    
    if passenger_data.embarked =='C':
        for i in [1,0,0]:
            passenger_array.append(i)
    elif passenger_data.embarked=='Q':
        for i in [0,1,0]:
            passenger_array.append(i)
    elif passenger_data.embarked=='S':
        for i in [0,0,1]:
            passenger_array.append(i)
    
    if passenger_data.p_class==1:
        for i in [1,0,0]:
            passenger_array.append(i)
    elif passenger_data.p_class==2:
        for i in [0,1,0]:
            passenger_array.append(i)
    elif passenger_data.p_class==3:
        for i in [0,0,1]:
            passenger_array.append(i)

    prediction= rf_model.predict([passenger_array])
    return {"Survived_result":int(prediction[0])}

