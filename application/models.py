from django.db import models


class transport_approval(models.Model):
    bill_id=models.CharField(max_length=100,primary_key=True)
    vehicle_no = models.CharField(max_length=100,blank=True,null=True)
    vehicle_type=models.CharField(max_length=100,blank=True,null=True)
    fule_type=models.CharField(max_length=100,blank=True,null=True)
    driver_id = models.CharField(max_length=100)
    buying_date = models.DateField(blank=True,null=True)
    Ending_KM = models.FloatField(blank=True,null=True)
    starting_KM = models.FloatField(blank=True,null=True)
    reason=models.CharField(max_length=500,blank=True,null=True)
    fuel_quantity = models.IntegerField(blank=True,null=True)
    route = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)
    Mileage = models.CharField(max_length=50,blank=True,null=True)
    proof_date=models.CharField(max_length=500,blank=True,null=True)



class Master_Vechicle(models.Model):
    vehicle_no = models.CharField(max_length=100,primary_key=True)
    Usage =models.CharField(max_length=100,blank=True,null=True)
    Driver_Name=models.CharField(max_length=100,blank=True,null=True)
    fule_type = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100,blank=True,null=True)
    Driver_Number = models.CharField(max_length=100,blank=True,null=True)
    route_name = models.CharField(max_length=1000,blank=True,null=True)
    