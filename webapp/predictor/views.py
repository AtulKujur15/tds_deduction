from django.db import models
from django.shortcuts import render
import joblib
import os
from .models import Prediction

# Load ML model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "..", "model", "tds_model.pkl")

model = joblib.load(model_path)


def home(request):
    return render(request, "index.html")


from .models import Prediction

def predict(request):

    if request.method == "POST":

        payment = int(request.POST['payment'])

        amount = float(request.POST['amount'])

        vendor = int(request.POST['vendor'])

        pan = int(request.POST['pan'])

        lower_certificate = int(request.POST['lower_certificate'])


        sample = [[payment, amount, vendor, pan]]

        rate = model.predict(sample)[0]


        # PAN rule (Section 206AA)
        if pan == 0:
            rate = 20


        # Lower deduction certificate rule
        if lower_certificate == 1:
            rate = rate / 2


        tds = amount * rate / 100


        # Calculate gross income for vendor
        gross = Prediction.objects.filter(
            vendor_type=vendor
        ).aggregate(total=models.Sum('amount'))


        gross_income = gross['total'] if gross['total'] else 0

        gross_income += amount


        # Save record
        Prediction.objects.create(

            payment_type=payment,

            amount=amount,

            vendor_type=vendor,

            pan_available=pan,

            lower_deduction_certificate=lower_certificate,

            gross_income=gross_income,

            tds_rate=rate,

            tds_amount=tds
        )


        return render(request, "result.html", {

            "rate": rate,

            "tds": tds,

            "gross_income": gross_income
        })

import csv
from django.http import HttpResponse
from .models import Prediction

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tds_predictions.csv"'

    writer = csv.writer(response)

    writer.writerow(['Payment Type','Amount','Vendor Type','TDS Rate','TDS Amount','Date'])

    data = Prediction.objects.all()

    for p in data:
        writer.writerow([p.payment_type,p.amount,p.vendor_type,p.tds_rate,p.tds_amount,p.created_at])

    return response