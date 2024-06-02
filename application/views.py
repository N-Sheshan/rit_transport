from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
import pandas as pd
from application.form import fuel_bill_detials,KM_update,Register_new_vechical,userform,loginform
from application.models import transport_approval,Master_Vechicle,User
from django.db.models import Q
from django.template.loader import render_to_string
from django.db.models import Sum, Min, Max, F,Avg,ExpressionWrapper, CharField, Case, When
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib.auth import logout
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
import io
from io import BytesIO
import qrcode
from reportlab.lib import pdfencrypt
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




def encrypt_password(raw_password):
    # Implement your password encryption algorithm (e.g., using hashlib)
    import hashlib
    return hashlib.sha256(raw_password.encode()).hexdigest()

def signup(request): 
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.Password=encrypt_password(form.cleaned_data['Password'])
            user.conform_Password =encrypt_password(form.cleaned_data['conform_Password'])
            user.save()
            request.session['user_auth'] = True
            user_data=request.session.get('user_auth')
            if user_data:
                 return redirect('fuel_application')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            data = User.objects.filter(email=form.cleaned_data['email']).first()
            if data:
                if encrypt_password(form.cleaned_data['Password']) == data.Password:
                    request.session['user_auth'] = True
                    return redirect('fuel_application')
                else:
                    return render(request, "login.html", {"error_message": "username or password is incorrect"})
            else:
                return render(request, "login.html", {"error_message": "the user data is not exist in db. So signup your account"})
    return render(request, 'login.html')

def logout_view(request):
    user_data=request.session.get('user_auth')
    if user_data :
        request.session['user_auth'] = False
        # logout(request)
        return redirect('login')


def fuel_application(request):
    if request.session.get('user_auth'):
        vechical = Master_Vechicle.objects.all()
        current_year = datetime.now().year
        current_month = datetime.now().strftime('%m')
        
        if request.method == 'POST':
            form = fuel_bill_detials(request.POST)
            if form.is_valid():
                vehicle_no = form.cleaned_data['vehicle_no']
                data = transport_approval.objects.filter(buying_date__year=current_year, buying_date__month=current_month)
                master_data = Master_Vechicle.objects.filter(vehicle_no=vehicle_no).first()  # Get the first instance or None
                billed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if master_data and form.cleaned_data['status'] == "Yes":
                    count = data.count()
                    user = form.save(commit=False)
                    bill_id='RIT'+str(current_year) + str(current_month) + f'{count + 1:03d}'
                    user.engine_oil_quantity =  user.engine_oil_quantity if  user.engine_oil_quantity.isnumeric() else 'None'
                    user.grease_quantity =  user.grease_quantity if  user.grease_quantity.isnumeric() else 'None'
                    user.distilled_water_quantity =  user.distilled_water_quantity if  user.distilled_water_quantity.isnumeric() else 'None'
                    user.bill_id = bill_id
                    user.vehicle_type = master_data.vehicle_type
                    user.fule_type = master_data.fule_type
                    user.route = master_data.route_name
                    user.billed_date = billed_date
                    user.save()
                    return render(request, "index.html", {"vechical": vechical, "success": "Bill details have been successfully submitted.",'bill_id':bill_id})
                else:
                    return render(request, "index.html", {"vechical": vechical, 'error_message': 'Vehicle not found or approval not given'})
            else:
                return render(request, "error.html", {'form': form})
        
        return render(request, "index.html", {"vechical": vechical})
    else:
         return redirect('login')


def data_update(request):
    if request.session.get('user_auth'):
        vechical = Master_Vechicle.objects.all()
        if request.method == 'POST':
            bill_id = request.POST.get('bill_id')
            km =  request.POST.get('Ending_KM')
            proof_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vechical_filter = get_object_or_404(transport_approval, bill_id=bill_id)
            vehicle_no = vechical_filter.vehicle_no
            date = vechical_filter.billed_date
            if vechical_filter.starting_KM is None:
                vechical_list = transport_approval.objects.filter(vehicle_no=vehicle_no, billed_date__lte=date).order_by('billed_date')
                form = KM_update(request.POST, instance=vechical_filter)
                if len(vechical_list) < 2:
                    if form.is_valid():
                        forms = form.save(commit=False)
                        data = Master_Vechicle.objects.filter(vehicle_no=vehicle_no).first()
                        start_km = data.Previous_km
                        vechical_filter.starting_KM = start_km
                        end_km=form.cleaned_data['Ending_KM']
                        forms.Mileage = round((float(end_km) - float(start_km)) / form.cleaned_data['fuel_quantity'], 2)
                        forms.proof_date = proof_date
                        vechical_filter.save()
                        forms.save()
                        return render(request, "data_upload.html", {'form': form,"vechical": vechical,'success': f"The Kilometer have been successfully update in the respative Bill ID"})
                    
                    else:
                        print(form.errors)
                        return render(request, "error.html", {'form': form})
                    return render(request, "error.html", {'error': 'Not enough records to update the second last entry.'})
                else:
                    le= len(vechical_list)-2
                    book = vechical_list[le]
                   
                    if book.Ending_KM is not None:
                      
                        if float(km) >float(book.Ending_KM):
                            forms = form.save(commit=False)
                            forms.starting_KM = book.Ending_KM
                            forms.Ending_KM = km
                            forms.Mileage = round((float(km)-float(forms.starting_KM))/forms.fuel_quantity,2)
                            forms.proof_date = proof_date
                            # book.save()
                            form.save()
                          
                            return render(request, "data_upload.html", {'success': f"The Kilometer have been successfully update in the respative Bill ID","vechical": vechical,})
                        else:
                            return render(request, "data_upload.html", {'error_message': f"Entered Kilometer Lesser than Ending km ,Ceck it and Enter again","vechical": vechical})
                    else:
                        print("Error: Starting KM is None. So Upload the data in order")
                        return render(request, "data_upload.html", {'error_message': f"Starting KM is None.","vechical": vechical})
            else:
                return render(request, "data_upload.html", {'error_message': f"Kilometer already exists for this {bill_id} Bill ID, so data upload is not allowed","vechical": vechical})
        else:
            form = KM_update()
        
        return render(request, "data_upload.html", {'form': form,"vechical": vechical})
    else:
        return redirect('login')

def get_bills_for_vehicle(request, vehicle_no):
    if request.session.get('user_auth'):
        bills = transport_approval.objects.filter(vehicle_no=vehicle_no,starting_KM__isnull=True).values_list('bill_id', flat=True).distinct()
        return JsonResponse({'bills': list(bills)})
    else:
        return redirect('login')

# Define the MONTH_NAMES dictionary
MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
def history(request):
    if request.session.get('user_auth'):
        data = transport_approval.objects.all()
        vechical = Master_Vechicle.objects.all()

        if request.method == 'POST':
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            vehicle_nos = request.POST.getlist('vehicle_no')  
            formate = request.POST.get('data_formate')  
            # month_numbers = [date.month for date in pd.date_range(from_date, to_date, freq='MS')]
            # month = MONTH_NAMES.get(max(month_numbers))
            if formate == 'cumulative':
                aggregated_data = []
                if vehicle_nos:
                    for vehicle_number in vehicle_nos:
                        if transport_approval.objects.filter(vehicle_no=vehicle_number, buying_date__range=[from_date, to_date]).exists():
                            data = transport_approval.objects.filter(
                                vehicle_no=vehicle_number,
                                buying_date__range=[from_date, to_date]
                            ).annotate(month_number=ExtractMonth('buying_date')).aggregate(  
                                average_mileage=Avg((F('Ending_KM') - F('starting_KM')) / F('fuel_quantity')),
                                total_fuel=Sum('fuel_quantity'),
                                start_km=Min('starting_KM'),
                                end_km=Max('Ending_KM'),
                                total_km = (Max('Ending_KM') - Min('starting_KM')),  
                              )  
                          
                            data['average_mileage'] = round(data['average_mileage'], 2)
                            
                            aggregated_data.append(data)
                            additional_data = transport_approval.objects.filter(vehicle_no=vehicle_number,buying_date__range=[from_date, to_date]).values_list('vehicle_no','vehicle_type','fule_type','route').first()

        
                            data['additional_data'] = additional_data
               
                return render(request, 'history.html', {'data':aggregated_data ,'vechical': vechical,'cumulative':True})
            else:
                data = data.filter(vehicle_no__in=vehicle_nos,buying_date__range=[from_date, to_date])
                context = {'data': data, 'vechical': vechical,'individual':True}
                return render(request, 'history.html', context)
        return render(request, 'history.html', {'vechical': vechical,'data': data,'individual':True})
    else:
        return redirect('login')



def new_vechical(request):
    if request.session.get('user_auth'):
        if request.method == 'POST':
            form = Register_new_vechical(request.POST)
            if form.is_valid():
                form.save()
                return render(request, "new_vechical.html", {'success': f"The New vechicle Details are Submitted successfully "})
            else:
                return render(request, "new_vechical.html", {'error_message': f"Entered vechical Number is already exist in the table, check vechical No"})
        return render(request, "new_vechical.html")
    else:
        return redirect('login')



import io
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import hashlib
import qrcode
from django.http import HttpResponse
from django.shortcuts import redirect

def hash_function(value, algorithm='sha256'):
    salt = "audit"
    value_bytes = str(value).encode()
    salt_bytes = salt.encode()
    salted_value = salt_bytes + value_bytes
    hash_func = hashlib.new(algorithm)
    hash_func.update(salted_value)
    return hash_func.hexdigest()

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_pdf(request, bill_id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    referer = request.META.get('HTTP_REFERER')
    path = referer.split('/')[-1] if referer is not None else None

    # Fetch data from the database
    data = transport_approval.objects.filter(bill_id=bill_id).first()
    if request.session.get('user_auth'):
        value = f'N.Govindaraju / 2500 K.S Selvaraj / 2369 {data.bill_id} {data.billed_date}'
        qr_data = f'{value}\n\n{hash_function(value)}'
        
        qr_buffer = generate_qr_code(qr_data)
        qr_img = ImageReader(qr_buffer)

        # Register fonts
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'C:/Windows/Fonts/times.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', 'C:/Windows/Fonts/timesbd.ttf'))

        # Add watermark text
        watermark_text = "Ramco Institute of Technology"
        p.setFont("TimesNewRoman", 36)
        p.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray color for the watermark
        p.saveState()
        p.translate(300, 613)
        p.rotate(33)
        p.drawCentredString(0, 0, watermark_text)
        p.restoreState()

        # Title
        p.setFont("TimesNewRoman-Bold", 13)
        p.setFillColorRGB(0, 0, 0)
        p.drawString(190, height - 30, "Ramco Institute of Technology")
        p.setFont("TimesNewRoman", 12)
        p.drawString(240, height - 42, "Rajapalayam")
        p.drawString(220, height - 54, "Fuel Requisition Slip")
        p.setFont("TimesNewRoman-Bold", 12)
        p.drawString(370, height - 75, 'Recipt No :')
        p.drawString(430, height - 75, data.bill_id)
        p.setFont("TimesNewRoman-Bold", 12)
        p.drawString(70, height - 80, "To :")
        p.setFont("TimesNewRoman", 10)
        p.drawString(100, height - 100, "P.A.C.R. SETHURAMAMMAL CHARITY TRUST,")
        p.drawString(100, height - 111, "BPCL, DEALERS @ 236463,")
        p.drawString(100, height - 122, "P.A.C. RAMASAMY RAJASALAI, RAJAPALAYAM.")

        # Car Details
        p.setFont("TimesNewRoman-Bold", 10)
        p.drawString(100, height - 150, "Please Supply for vehicle No")
        p.drawString(260, height - 150, ":")
        p.drawString(270, height - 150, data.vehicle_no)
        p.drawString(370, height - 130, "Date&Time")
        p.drawString(425, height - 130, ":")
        p.drawString(430, height - 130, data.billed_date)
        
        # Items
        p.setFont("TimesNewRoman-Bold", 10)
        p.drawString(130, height - 170, "Fuel Type")
        p.drawString(260, height - 170, ":")
        p.drawString(270, height - 170, data.fule_type)

        p.drawString(130, height - 190, "Vehicle Type")
        p.drawString(260, height - 190, ":")
        p.drawString(270, height - 190, data.vehicle_type)

        p.drawString(130, height - 210, "Fuel Quantity")
        p.drawString(260, height - 210, ":")
        p.drawString(270, height - 210, "Tank Full")

        p.drawString(130, height - 230, "Engine Oil")
        p.drawString(260, height - 230, ":")
        if data.engine_oil_quantity == 'None':
            p.drawString(270, height - 230, 'None')
        else:
            p.drawString(270, height - 230, data.engine_oil_quantity + ' Liter')

        p.drawString(130, height - 250, "Grease Type")
        p.drawString(260, height - 250, ":")
        p.drawString(270, height - 250, data.grease_company)

        p.drawString(130, height - 265, "Grease")
        p.drawString(260, height - 265, ":")
        if data.grease_quantity == 'None':
            p.drawString(270, height - 265, 'None')
        else:
            p.drawString(270, height - 265, data.grease_quantity + ' kG')

        p.drawString(130, height - 280, "Distilled Water")
        p.drawString(260, height - 280, ":")
        if data.distilled_water_quantity == 'None':
            p.drawString(270, height - 280, 'None')
        else:
            p.drawString(270, height - 280, data.distilled_water_quantity + ' Liter')

        # Signature and Address
        p.setFont("TimesNewRoman-Bold", 12)
        p.drawString(110, height - 320, "Transport Incharge")
        p.drawString(420, height - 320, "GM Admin")
        p.setFont("TimesNewRoman", 11)
        p.drawString(100, height - 334, "( N.Govindaraju / 2500 )")
        p.drawString(410, height - 334, "( Selva Raj / 2369 )")
        
        # Rectangle for the main content
        p.rect(50, 450, 500, 330)

        # Seal (simulated by drawing an ellipse and text)
        image_path = "static/images/imag1.jpg"
        if os.path.isfile(image_path):
            img = Image.open(image_path)
            img_reader = ImageReader(img)
            p.drawImage(img_reader, 340, height - 330, width=70, height=70)

        # Draw QR Code Image
        p.drawImage(qr_img, 400, height - 250, width=100, height=100) 

        # Finalize the PDF
        p.showPage()
        p.save()

        # Get the value of the buffer and close it
        pdf = buffer.getvalue()
        buffer.close()

        # Create the HttpResponse object with the appropriate PDF headers
        response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="{bill_id}.pdf"'   # This will prompt a download

        return response
    else:
        if path is None:
            return redirect('login')
        else:
            return redirect(f'{path}')



@csrf_exempt
def qr_scanner(request):
    if request.method == 'POST':
        print('--------------------------------- qr scanner working')
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data')
            print('--------------------------------- ',qr_data)
            rit_pattern = r'RIT\d{9}'
            hash_pattern = r'[a-f0-9]{64}'
            # Find all matches
            rit_match = re.search(rit_pattern, qr_data)
            hash_match = re.search(hash_pattern, qr_data)
            # Extract the values if found
            rit_value = rit_match.group(0) if rit_match else None
            hash_value = hash_match.group(0) if hash_match else None
            print("Extracted RIT value:", rit_value)
            print("Extracted Hash value:", hash_value)
            db_data = transport_approval.objects.filter(bill_id=rit_value).first()
            if rit_value is not None and db_data:
                print('+++',db_data.bill_id)
                # s_value = f'N.Govindaraju / 2500 K.S Selvaraj / 2369 {db_data.bill_id} {db_data.billed_date}'
                s_value = f'N.Govindaraju / 2500 Selva Raj / 2369 {db_data.bill_id} {db_data.billed_date}'
                if hash_function(s_value) == hash_value:
                    success = True
                    return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error_message': 'Invalid QR Code'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error_message': 'Invalid data'})
    return render(request, 'qr_reader.html')
