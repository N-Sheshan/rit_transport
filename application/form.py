from django import forms
from .models import transport_approval,Master_Vechicle,User,power_station_approval


class fuel_bill_detials(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['vehicle_no','driver_id','buying_date','reason','status','engine_oil_quantity','grease_company','grease_quantity','distilled_water_quantity']
        exclude=['bill_id','vehicle_type','fule_type','route','billed_date']


class KM_update(forms.ModelForm):
    class Meta:
        model = transport_approval
        fields = ['bill_id','Ending_KM','fuel_quantity']
        exclude=["starting_KM","Mileage",'proof_date']


class Register_new_vechical(forms.ModelForm):
    class Meta:
        model = Master_Vechicle
        fields = ['vehicle_no','Usage','Driver_Name',"fule_type","vehicle_type",'Driver_Number','route_name','Previous_km']
        
class userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Name','email','Password','conform_Password']

class loginform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','Password']

class ps_fuel_form(forms.ModelForm):
    class Meta:
        model = power_station_approval
        fields = ['generater_no','buying_date','fule_type','reason','fuel_quantity','status']
        exclude=["billed_date",'bill_id']