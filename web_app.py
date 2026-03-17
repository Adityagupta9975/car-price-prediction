import flask
from flask import Flask, render_template, request, flash, jsonify, session
import pickle

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'


# Load model and scaler once
with open('saved_models/RandomForestRegressor.pkl', 'rb') as f:
    model = pickle.load(f)

with open('saved_scaling/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


def format_value(value):
    if value >= 10000000:
        return f"{value / 10000000:.2f} Cr"
    elif value >= 100000:
        return f"{value / 100000:.2f} Lakhs"
    else:
        return f"{value:,.0f}" if value >= 1000 else str(value)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json or request.form
        vehicle_age = int(data.get('vehicle_age', 0))
        km_driven = int(data.get('km_driven', 0))
        mileage = float(data.get('mileage', 0))
        engine = int(data.get('engine', 0))
        max_power = float(data.get('max_power', 0))
        seats = int(data.get('seats', 0))

        if not (1 <= seats <= 7):
            raise ValueError('Seats must be between 1 and 7')

        seller_type = data.get('seller_type', 'Dealer')
        fuel_type = data.get('fuel_type', 'Petrol')
        transmission = data.get('transmission', 'Manual')

        seller_map = {'Dealer': [1, 0, 0], 'Individual': [0, 1, 0], 'Trustmark Dealer': [0, 0, 1]}
        fuel_map = {
            'CNG': [1, 0, 0, 0, 0],
            'Diesel': [0, 1, 0, 0, 0],
            'Electric': [0, 0, 1, 0, 0],
            'LPG': [0, 0, 0, 1, 0],
            'Petrol': [0, 0, 0, 0, 1],
        }
        trans_map = {'Automatic': [1, 0], 'Manual': [0, 1]}

        features = [vehicle_age, km_driven, mileage, engine, max_power, seats]
        features += seller_map.get(seller_type, [0, 0, 0])
        features += fuel_map.get(fuel_type, [0, 0, 0, 0, 0])
        features += trans_map.get(transmission, [0, 1])

        if len(features) != 16:
            raise ValueError('Invalid feature vector length')

        scaled = scaler.transform([features])
        prediction = model.predict(scaled)[0]
        pred_text = f'₹ {format_value(prediction)}'

        # session-based history
        history = session.get('history', [])
        history.insert(0, {
            'name': data.get('car_name', 'Car'),
            'price': pred_text,
            'details': f'{vehicle_age} yrs, {km_driven} km, {fuel_type}, {transmission}'
        })
        session['history'] = history[:10]

        return jsonify(success=True, result=pred_text, history=session['history'])
    except Exception as e:
        return jsonify(success=False, error=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True)
