from django import forms
from .models import transport_approval


class fuel_bill_detials(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['vechical_no','driver_id','buying_date','reason','fuel_amount','status']
        exclude=['bill_id','vechical_type','fule_type','route']


class KM_update(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['bill_id','overall_km']
