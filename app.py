# app.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Stock recommendations based on risk type
STOCKS = {
    "low": [
        {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
        {"name": "Infosys", "ticker": "INFY.NS"},
        {"name": "ITC Ltd", "ticker": "ITC.NS"},
        {"name": "Tata Consultancy Services", "ticker": "TCS.NS"},
        {"name": "Hindustan Unilever", "ticker": "HINDUNILVR.NS"},
    ],
    "medium": [
        {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
        {"name": "Bharti Airtel", "ticker": "BHARTIARTL.NS"},
        {"name": "ICICI Bank", "ticker": "ICICIBANK.NS"},
        {"name": "Larsen & Toubro", "ticker": "LT.NS"},
        {"name": "Axis Bank", "ticker": "AXISBANK.NS"},
    ],
    "high": [
        {"name": "Zomato", "ticker": "ZOMATO.NS"},
        {"name": "Paytm", "ticker": "PAYTM.NS"},
        {"name": "Nykaa", "ticker": "NYKAA.NS"},
        {"name": "Adani Enterprises", "ticker": "ADANIENT.NS"},
        {"name": "Tata Motors", "ticker": "TATAMOTORS.NS"},
    ],
}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to StockSphere API", "status": "Running"})

@app.route("/recommend", methods=["POST"])
def recommend_stocks():
    data = request.get_json()

    # Extract inputs
    age_group = data.get("age_group")
    experience = data.get("experience")
    horizon = data.get("horizon")
    risk = data.get("risk_tolerance", "medium").lower()

    # Select stock list based on risk level
    stocks = STOCKS.get(risk, STOCKS["medium"])
    recommendations = random.sample(stocks, 3)

    response = {
        "profile": {
            "age_group": age_group,
            "experience": experience,
            "horizon": horizon,
            "risk_tolerance": risk
        },
        "recommendations": recommendations
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
