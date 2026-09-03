
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# 12 features (9 clinical + 3 genetic risk-allele counts)
FEATURES = [
    "Age", "BMI", "Glucose", "Insulin", "HOMA",
    "Leptin", "Adiponectin", "Resistin", "MCP.1",
    "RA_SNP1", "RA_SNP2", "RA_SNP3"
]

# Means and STDs chosen around clinically plausible ranges, to stabilize scaling
MEANS = np.array([
    48.0, 27.0, 110.0, 10.0, 2.7,
    15.0,  9.0,  8.0, 420.0,
     1.0,  1.0,  1.0
], dtype=float)

STDS = np.array([
    18.0, 6.0, 28.0, 5.0, 2.0,
     8.0, 4.0, 3.0, 120.0,
     0.7, 0.7, 0.7
], dtype=float)

# Coefficients: positive for risk-raising factors, negative for protective ones.
# Tuned to give a good spread of probabilities, incorporating genetics too.
COEFS = np.array([
    0.18,   # Age
    0.35,   # BMI
    0.55,   # Glucose
    0.25,   # Insulin
    0.25,   # HOMA
    0.08,   # Leptin
   -0.30,   # Adiponectin (protective)
    0.20,   # Resistin
    0.10,   # MCP.1
    0.40,   # RA_SNP1
    0.32,   # RA_SNP2
    0.28    # RA_SNP3
], dtype=float)

# Intercept such that a "typical" profile lands near mid risk (~40–50%)
INTERCEPT = -0.35

def safe_float(x, default=0.0):
    try:
        if x is None:
            return default
        if isinstance(x, str) and x.strip() == "":
            return default
        return float(x)
    except Exception:
        return default

def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + np.exp(-z))

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "features": FEATURES})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True) or {}
        # Build x in FEATURE order; default genetics to 0 if omitted
        vals = []
        for name in FEATURES:
            default = 0.0 if name.startswith("RA_SNP") else 0.0
            vals.append(safe_float(data.get(name, default)))
        x = np.array(vals, dtype=float)

        # Standardize and score
        z = ((x - MEANS) / STDS) @ COEFS + INTERCEPT
        p = float(sigmoid(z))
        risk_percent = round(p * 100.0, 2)

        if risk_percent < 34:
            risk_type = "Low"
        elif risk_percent < 67:
            risk_type = "Medium"
        else:
            risk_type = "High"

        prediction = "Diabetic" if p >= 0.5 else "Non-Diabetic"

        return jsonify({
            "prediction": prediction,
            "risk_type": risk_type,
            "risk_percent": risk_percent
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Runs on 127.0.0.1:5000 by default
    app.run(host="127.0.0.1", port=5000, debug=True)
