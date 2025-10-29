from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)

# ✅ Configure CORS properly
CORS(app, 
     origins=[
         "https://stocksphere-kappa.vercel.app", 
         "http://localhost:3000",
         "http://localhost:3001"
     ],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stock recommendation database
STOCK_RECOMMENDATIONS = {
    "low": [
        {"name": "HDFC Bank", "ticker": "HDFCBANK", "sector": "Banking"},
        {"name": "Infosys", "ticker": "INFY", "sector": "IT"},
        {"name": "ITC Limited", "ticker": "ITC", "sector": "FMCG"},
        {"name": "Asian Paints", "ticker": "ASIANPAINT", "sector": "Paints"},
    ],
    "medium": [
        {"name": "Reliance Industries", "ticker": "RELIANCE", "sector": "Conglomerate"},
        {"name": "Tata Consultancy Services", "ticker": "TCS", "sector": "IT"},
        {"name": "ICICI Bank", "ticker": "ICICIBANK", "sector": "Banking"},
        {"name": "Larsen & Toubro", "ticker": "LT", "sector": "Engineering"},
    ],
    "high": [
        {"name": "Adani Enterprises", "ticker": "ADANIENT", "sector": "Infrastructure"},
        {"name": "Zomato", "ticker": "ZOMATO", "sector": "Food Tech"},
        {"name": "Paytm", "ticker": "PAYTM", "sector": "Fintech"},
        {"name": "Nykaa", "ticker": "NYKAA", "sector": "E-commerce"},
    ]
}

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "message": "Welcome to StockSphere API!",
        "version": "1.0",
        "endpoints": {
            "recommend": "POST /recommend",
            "health": "GET /"
        }
    }), 200

@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    """Main recommendation endpoint"""
    
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return "", 204
    
    try:
        # Get and validate JSON data
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({
                "error": "No data provided",
                "message": "Request body must contain JSON data"
            }), 400
        
        # Extract user inputs with validation
        age_group = data.get("age_group", "")
        experience = data.get("experience", "")
        horizon = data.get("horizon", "")
        risk_tolerance = data.get("risk_tolerance", "")
        
        logger.info(f"Received request: age={age_group}, exp={experience}, horizon={horizon}, risk={risk_tolerance}")
        
        # Validate required fields
        if not all([age_group, experience, horizon, risk_tolerance]):
            return jsonify({
                "error": "Missing required fields",
                "message": "All fields (age_group, experience, horizon, risk_tolerance) are required"
            }), 400
        
        # Normalize risk tolerance
        risk_key = risk_tolerance.lower()
        
        # Get recommendations based on risk tolerance
        recommendations = STOCK_RECOMMENDATIONS.get(
            risk_key, 
            STOCK_RECOMMENDATIONS["medium"]
        )
        
        # Build profile object
        profile = {
            "age_group": age_group,
            "experience": experience,
            "horizon": horizon,
            "risk_tolerance": risk_tolerance,
        }
        
        # Return response
        response = {
            "success": True,
            "profile": profile,
            "recommendations": recommendations,
            "message": f"Generated {len(recommendations)} recommendations for {risk_tolerance} risk profile"
        }
        
        logger.info(f"Returning {len(recommendations)} recommendations")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "service": "StockSphere API",
        "version": "1.0"
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
