from django import forms
from .models import transport_approval


class fuel_bill_detials(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['vehicle_no','driver_id','buying_date','reason','fuel_quantity','status']
        exclude=['bill_id','vehicle_type','fule_type','route']


class KM_update(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['bill_id','starting_KM']
        exclude=["Ending_KM","Mileage",'proof_date']
