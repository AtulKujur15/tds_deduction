from django.db import models

class Prediction(models.Model):

    payment_type = models.CharField(max_length=50)

    amount = models.FloatField()

    vendor_type = models.CharField(max_length=50)

    pan_available = models.BooleanField()

    lower_deduction_certificate = models.BooleanField(default=False)

    gross_income = models.FloatField(null=True)

    tds_rate = models.FloatField()

    tds_amount = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_type} - {self.amount}"