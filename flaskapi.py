from flask import Flask, render_template
import numpy as np
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired
import pickle
import json

def Predict_Price(location, total_sqft, bathrooms, bhk):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(data_columns))
    x[0] = total_sqft
    x[1] = bathrooms
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return model.predict([x])[0]

with open('banglore_home_prices_model.pickle', 'rb') as f:
    model = pickle.load(f)
    print("Model is downloaded...")

with open('columns.json') as f:
    data_columns = json.load(f)['data_columns']
    print('Data is loaded...')

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

class PredictionForm(FlaskForm):
    location = SelectField('Location', choices=data_columns[3:])
    total_sqft = FloatField('Square Foot Value', validators=[DataRequired()])
    bathrooms = FloatField('No. of Bathrooms', validators=[DataRequired()])
    bhk = IntegerField('No. of BHK', validators=[DataRequired()])
    submit = SubmitField('Predict')

@app.route('/', methods=['GET', 'POST'])
def home():
    global prediction
    form = PredictionForm()

    if form.validate_on_submit():
        location = form.location.data
        total_sqft = form.total_sqft.data
        bathrooms = form.bathrooms.data
        bhk = form.bhk.data

        prediction = Predict_Price(location, total_sqft, bathrooms, bhk)
        return render_template('index.html', form=form, prediction=prediction)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
