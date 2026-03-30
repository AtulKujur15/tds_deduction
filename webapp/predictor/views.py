import os
import joblib
from django.shortcuts import render

# =========================
# LOAD NLP MODEL (CORRECT PATH)
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

model_path = os.path.join(BASE_DIR, "model", "payment_text_model.pkl")

# Check if model exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at: {model_path}")

nlp_model = joblib.load(model_path)


# =========================
# HOME PAGE
# =========================

def home(request):
    return render(request, "index.html")


# =========================
# PREDICT FUNCTION
# =========================

def predict(request):

    if request.method == "POST":

        try:
            # -------------------------
            # GET INPUT FROM FORM
            # -------------------------
            description = request.POST.get("description", "")
            amount = float(request.POST.get("amount", 0))
            vendor = int(request.POST.get("vendor", 0))
            pan = int(request.POST.get("pan", 1))
            lower_certificate = int(request.POST.get("lower_certificate", 0))

            # -------------------------
            # NLP MODEL PREDICTION
            # -------------------------
            payment_type = nlp_model.predict([description])[0]

            # -------------------------
            # TDS RATE LOGIC
            # -------------------------
            rate_map = {
                "rent": 10,
                "professional": 10,
                "contractor": 2,
                "interest": 10
            }

            rate = rate_map.get(payment_type, 10)

            # -------------------------
            # PAN RULE (Section 206AA)
            # -------------------------
            if pan == 0:
                rate = 20

            # -------------------------
            # LOWER DEDUCTION (Section 197)
            # -------------------------
            if lower_certificate == 1:
                rate = rate / 2

            # -------------------------
            # TDS CALCULATION
            # -------------------------
            tds = amount * rate / 100

            # -------------------------
            # RETURN RESULT
            # -------------------------
            return render(request, "result.html", {
                "payment_type": payment_type.capitalize(),
                "rate": rate,
                "tds": round(tds, 2),
                "amount": amount
            })

        except Exception as e:
            return render(request, "result.html", {
                "payment_type": "Error",
                "rate": 0,
                "tds": 0,
                "amount": 0,
                "error": str(e)
            })

    return render(request, "index.html")