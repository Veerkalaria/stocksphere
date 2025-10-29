from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# ✅ Allow frontend requests
CORS(app, origins=["https://stocksphere-kappa.vercel.app", "http://localhost:3000"])

@app.route("/", methods=["POST"])
def recommend():
    data = request.get_json()

    # Extract user inputs
    age_group = data.get("age_group", "")
    experience = data.get("experience", "")
    horizon = data.get("horizon", "")
    risk_tolerance = data.get("risk_tolerance", "")

    # Simple rule-based logic (replace with your model later)
    if risk_tolerance.lower() == "low":
        recommendations = [
            {"name": "HDFC Bank", "ticker": "HDFCBANK"},
            {"name": "Infosys", "ticker": "INFY"},
        ]
    elif risk_tolerance.lower() == "medium":
        recommendations = [
            {"name": "Reliance Industries", "ticker": "RELIANCE"},
            {"name": "Tata Consultancy Services", "ticker": "TCS"},
        ]
    else:
        recommendations = [
            {"name": "Adani Enterprises", "ticker": "ADANIENT"},
            {"name": "Zomato", "ticker": "ZOMATO"},
        ]

    profile = {
        "age_group": age_group,
        "experience": experience,
        "horizon": horizon,
        "risk_tolerance": risk_tolerance,
    }

    return jsonify({"profile": profile, "recommendations": recommendations})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to StockSphere API!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
