from django.db import models


class transport_approval(models.Model):
    bill_id=models.CharField(max_length=100,primary_key=True)
    vechical_no = models.CharField(max_length=100)
    vechical_type=models.CharField(max_length=100)
    fule_type=models.CharField(max_length=100)
    driver_id = models.CharField(max_length=100)
    buying_date = models.DateField()
    overall_km = models.FloatField()
    reason=models.CharField(max_length=500)
    fuel_amount = models.IntegerField()
