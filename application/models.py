from django.db import models


class transport_approval(models.Model):
    bill_id=models.CharField(max_length=100,primary_key=True)
    vechical_no = models.CharField(max_length=100,blank=True,null=True)
    vechical_type=models.CharField(max_length=100,blank=True,null=True)
    fule_type=models.CharField(max_length=100,blank=True,null=True)
    driver_id = models.CharField(max_length=100)
    buying_date = models.DateField(blank=True,null=True)
    overall_km = models.FloatField(blank=True,null=True)
    reason=models.CharField(max_length=500,blank=True,null=True)
    fuel_amount = models.IntegerField(blank=True,null=True)
    route = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)