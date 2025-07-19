# app.py

from flask import Flask, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

app = Flask(__name__)
model = load_model('stock_model.h5')

@app.route('/recommendation')
def get_recommendation():
    df = yf.download('AAPL', start='2018-01-01', end='2024-01-01')
    close_prices = df['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(close_prices)

    seq_length = 50
    last_sequence = scaled_data[-seq_length:].reshape(1, seq_length, 1)

    predictions = []
    for _ in range(7):
        next_price = model.predict(last_sequence)[0][0]
        predictions.append(next_price)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[next_price]]], axis=1)

    predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    current_price = close_prices[-1][0]
    future_avg = np.mean(predicted_prices)

    recommendation = "BUY" if future_avg > current_price else "SELL"
    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)
