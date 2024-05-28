from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
import pandas as pd
from application.form import fuel_bill_detials,KM_update,Register_new_vechical,userform
from application.models import transport_approval,Master_Vechicle,User
from django.db.models import Q
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from openpyxl import Workbook
import pdfkit
from xhtml2pdf import pisa
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
import io
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from PyPDF2 import PdfFileReader, PdfFileWriter
# Create your views here.

def encrypt_password(raw_password):
    # Implement your password encryption algorithm (e.g., using hashlib)
    import hashlib
    return hashlib.sha256(raw_password.encode()).hexdigest()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('----------------------------', email, password)
        user = User.objects.filter(email=email).first()
        if user:
            if user.Password == encrypt_password(password):
                return redirect('fuel_application')
    

    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            password = form.cleaned_data['Password']
            confirm_password = form.cleaned_data['conform_Password']
            email =  form.cleaned_data['email']
            if password == confirm_password:
                encrypted_password = encrypt_password(password)

                # Save the encrypted password to your user model
                data = User.objects.filter(email=email).first()
                if data:
                    form.add_error('email', 'email id is already exist')
                    return render(request, "signup.html", {'form': form})
                else:
                    user = form.save(commit=False)  # Don't save the form yet
                    user.Password = encrypted_password
                    user.conform_Password = encrypted_password

                    user.save()

                # Redirect to a success page or login page
                    return redirect('login')
                # return render(request,'login.html')
            else:
                # Passwords don't match, return an error
                form.add_error('conform_Password', 'Passwords do not match')
                return render(request, "signup.html", {'form': form})
        else:
            return render(request, "signup.html", {'form': form})
    else:
        form = userform()
        return render(request, "signup.html")
def fuel_application(request):
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
                user.bill_id = bill_id
                user.vehicle_type = master_data.vehicle_type
                user.fule_type = master_data.fule_type
                user.route = master_data.route_name
                user.billed_date = billed_date
                user.save()
            
                # return redirect(generate_pdf,bill_id)
                # return redirect(reverse('generate_pdf_view', kwargs={'bill_id': user.bill_id}))  
                return render(request, "index.html", {"vechical": vechical, "success": "Bill details have been successfully submitted.",'bill_id':bill_id})
            else:
                return render(request, "index.html", {"vechical": vechical, 'error_message': 'Vehicle not found or approval not given'})
        else:
            return render(request, "error.html", {'form': form})
    
    return render(request, "index.html", {"vechical": vechical})

def data_update(request):
    vechical = Master_Vechicle.objects.all()
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        km =  request.POST.get('Ending_KM')
        proof_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vechical_filter = get_object_or_404(transport_approval, bill_id=bill_id)
        vehicle_no = vechical_filter.vehicle_no
        date = vechical_filter.billed_date
        # print('+++++++++++++++++',vehicle_no)
        if vechical_filter.starting_KM is None:
            vechical_list = transport_approval.objects.filter(vehicle_no=vehicle_no, billed_date__lte=date).order_by('billed_date')
            # for s in vechical_list:
            #     print('#######',s.bill_id,'->',s.buying_date)
            form = KM_update(request.POST, instance=vechical_filter)
            if len(vechical_list) < 2:
                if form.is_valid():
                    forms = form.save(commit=False)
                    data = Master_Vechicle.objects.filter(vehicle_no=vehicle_no).first()
                    # print('-----------------------', len(data))
                    
                    start_km = data.Previous_km
                    # print('=================',vechical_filter.starting_KM)
                    vechical_filter.starting_KM = start_km
                    # print('=================',bill_id,vechical_filter.starting_KM)
                    end_km=form.cleaned_data['Ending_KM']
                    # end_km = form.cleaned_data['Ending_KM']
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
                # print('---------------------------')
                # print(f"Bill ID: {book.bill_id}")
                # print(f"Vehicle NO: {book.vehicle_no}")
                # print(f"Buying Date: {book.buying_date}")              
                # print(f"Buying Date: {book.starting_KM}")
                # print(f"Buying Date: {book.Ending_KM}")
                # print('--------------------------- km type and starting_KM', type(km) , type(book.starting_KM) )
                if book.Ending_KM is not None:
                    # print('^^^^^^^^^^^^^^^^^^^^^^^^^^^',km,book.Ending_KM)
                    if float(km) >float(book.Ending_KM):
                        forms = form.save(commit=False)
                        forms.starting_KM = book.Ending_KM
                        forms.Ending_KM = km
                        forms.Mileage = round((float(km)-float(forms.starting_KM))/forms.fuel_quantity,2)
                        forms.proof_date = proof_date
                        # book.save()
                        form.save()
                        # print('--------------------------- km type and starting_KM', type(float(km)) , type(float(book.starting_KM)) )
                        # print(f"Ending_KM: {book.Ending_KM}")
                        # print(f"Mileage: {book.Mileage}")
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

def get_bills_for_vehicle(request, vehicle_no):
    bills = transport_approval.objects.filter(vehicle_no=vehicle_no,starting_KM__isnull=True).values_list('bill_id', flat=True).distinct()
    # bills = transport_approval.objects.filter(
    #     Q(vehicle_no=vehicle_no) & (Q(starting_KM__isnull=True) | Q(starting_KM=None))
    # ).values_list('bill_id', flat=True).distinct()
    print('>>>>>', bills)
    return JsonResponse({'bills': list(bills)})


# from django.shortcuts import render
# from django.http import HttpResponse
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch



def history(request):
    data = transport_approval.objects.all()
    vechical = Master_Vechicle.objects.all()

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        vehicle_nos = request.POST.getlist('vehicle_no')  # Get multiple selected vehicles
        print('******************>',vehicle_nos,from_date,to_date)
        if from_date and to_date:
            data = data.filter(buying_date__range=[from_date, to_date])
        if vehicle_nos:
            data = data.filter(vehicle_no__in=vehicle_nos)

    context = {'data': data, 'vechical': vechical}
    return render(request, 'history.html', context)


def export_view(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        vehicle_nos = request.POST.getlist('vehicle_no')
        export_format = request.POST.get('format')
        print('******************',from_date,to_date,vehicle_nos,export_format)
        data = transport_approval.objects.all()  # Get your data (apply filters if needed)

        if from_date and to_date:
            data = data.filter(buying_date__range=[from_date, to_date])
        if vehicle_nos:
            data = data.filter(vehicle_no__in=vehicle_nos)

        if export_format == 'excel':
            response = export_to_excel(data)
        elif export_format == 'pdf':
            response = export_to_pdf(data)
        else:
            response = HttpResponse("Invalid export format")

        return response

def export_to_excel(data):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'

    wb = Workbook()
    ws = wb.active

    # Add headers
    headers = [
        'Bill ID', 'Vehicle No', 'Driver ID', 'Vehicle Type', 
        'Fuel Type', 'Buying Date', 'Reason', 'Fuel Quantity', 
        'Route', 'Starting KM', 'Ending KM', 'Mileage', 'Status'
    ]
    ws.append(headers)

    # Add data rows
    for item in data:
        ws.append([
            item.bill_id, item.vehicle_no, item.driver_id, item.vehicle_type,
            item.fuel_type, item.buying_date, item.reason, item.fuel_quantity,
            item.route, item.starting_KM, item.Ending_KM, item.Mileage, item.status
        ])

    wb.save(response)
    return response

def export_to_pdf(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exported_data.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("TimesNewRoman", 12)

    # ... (Logic to format and add data to the PDF)

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def new_vechical(request):
    if request.method == 'POST':
        print('------------------------')
        form = Register_new_vechical(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "new_vechical.html", {'success': f"The New vechicle Details are Submitted successfully "})
        else:
            return render(request, "new_vechical.html", {'error_message': f"Entered vechical Number is already exist in the table, check vechical No"})
    return render(request, "new_vechical.html")





def generate_pdf(request, bill_id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Fetch data from the database
    data = transport_approval.objects.filter(bill_id=bill_id).first()

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
    p.setFont("TimesNewRoman-Bold", 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(170, height - 50, "P.A.C.R. SETHURAMAMMAL CHARITY TRUST")
    p.setFont("TimesNewRoman", 10)
    p.drawString(230, height - 70, "BPCL, DEALERS @ 236463")
    p.drawString(180, height - 85, "P.A.C. RAMASAMY RAJASALAI, RAJAPALAYAM.")
    
    p.setFont("TimesNewRoman-Bold", 10)
    p.drawString(400, height - 30, 'No :')
    p.drawString(422, height - 30, data.bill_id)

    # Car Details
    p.setFont("TimesNewRoman-Bold", 10)
    p.drawString(100, height - 110, "Please Supply for vehicle No")
    p.drawString(260, height - 110, ":")
    p.drawString(270, height - 110, data.vehicle_no)
    p.drawString(380, height - 110, "Date&Time")
    p.drawString(435, height - 110, ":")
    p.drawString(440, height - 110, data.billed_date)
    
    # Items
    p.setFont("TimesNewRoman-Bold", 10)
    p.drawString(180, height - 140, "Fuel Type")
    p.drawString(265, height - 140, ":")
    p.drawString(276, height - 140, data.vehicle_type)

    p.drawString(180, height - 160, "Fuel Quantity")
    p.drawString(265, height - 160, ":")
    p.drawString(276, height - 160, "Tank Full")

    p.drawString(180, height - 180, "Engine Oil")
    p.drawString(265, height - 180, ":")
    if data.engine_oil_quantity == 'None':
        p.drawString(276, height - 180, 'None')
    else:
        p.drawString(276, height - 180, data.engine_oil_quantity + ' Liter')

    p.drawString(180, height - 200, "Grease Company")
    p.drawString(265, height - 200, ":")
    p.drawString(276, height - 200, data.grease_company)

    if data.grease_quantity != 'None':
        p.drawString(180, height - 220, "Grease")
        p.drawString(265, height - 220, ":")
        p.drawString(276, height - 220, data.grease_quantity + ' Liter')

    if data.grease_quantity == 'None' and data.distilled_water_quantity != 'None':
        p.drawString(180, height - 220, "Distilled Water")
        p.drawString(265, height - 220, ":")
        p.drawString(276, height - 220, data.distilled_water_quantity + ' Liter')
    else:
        p.drawString(180, height - 240, "Distilled Water")
        p.drawString(265, height - 240, ":")
        p.drawString(276, height - 240, 'None')

    # Signature and Address
    p.setFont("TimesNewRoman-Bold", 12)
    p.drawString(100, height - 300, "Transport Incharge")
    p.drawString(430, height - 300, "GM Admin")

    # Rectangle for the main content
    p.rect(50, 470, 500, 310)

    # Seal (simulated by drawing an ellipse and text)
    image_path = "static/images/imag1.jpg"
    if os.path.isfile(image_path):
        img = Image.open(image_path)
        img_reader = ImageReader(img)
        p.drawImage(img_reader, 340, height - 310, width=70, height=70)  # Adjust the coordinates and size as needed

    # Finalize the PDF
    p.showPage()
    p.save()

    # Get the value of the buffer and close it
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{bill_id}.pdf"'   # This will prompt a download

    return response


