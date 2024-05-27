from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import JsonResponse
import pandas as pd
from application.form import fuel_bill_detials,KM_update,Register_new_vechical
from application.models import transport_approval,Master_Vechicle
from django.db.models import Q
from django.template.loader import render_to_string
from openpyxl import Workbook
import pdfkit
from xhtml2pdf import pisa
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
# Create your views here.


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
                user.bill_id = 'RIT'+str(current_year) + str(current_month) + f'{count + 1:03d}'
                user.vehicle_type = master_data.vehicle_type
                user.fule_type = master_data.fule_type
                user.route = master_data.route_name
                user.billed_date = billed_date
                user.save()
                generate_pdf(request)
                # return redirect(reverse('generate_pdf_view', kwargs={'bill_id': user.bill_id}))  
                return render(request, "index.html", {"vechical": vechical, "success": "Bill details have been successfully submitted."})
            else:
                return render(request, "index.html", {"vechical": vechical, 'error_message': 'Vehicle not found or approval not given'})
        else:
            return render(request, "error.html", {'form': form})
    
    return render(request, "index.html", {"vechical": vechical})

def data_update(request):
    vechical = Master_Vechicle.objects.all()
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        km =  request.POST.get('starting_KM')
        proof_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vechical_filter = get_object_or_404(transport_approval, bill_id=bill_id)
        vehicle_no = vechical_filter.vehicle_no
        date = vechical_filter.buying_date
        # print('+++++++++++++++++',vehicle_no)
        if vechical_filter.starting_KM is None:
            vechical_list = transport_approval.objects.filter(vehicle_no=vehicle_no, billed_date__lte=date).order_by('billed_date')
            # for s in vechical_list:
            #     print('#######',s.bill_id,'->',s.buying_date)
            form = KM_update(request.POST, instance=vechical_filter)
            if len(vechical_list) < 2:
                if form.is_valid():
                    form.save()
                    return render(request, "data_upload.html", {'form': form,"vechical": vechical,'success': f"The Kilometer have been successfully update in the respative Bill ID"})
                else:
                    print(form.errors)
                    return render(request, "error.html", {'form': form})
                return render(request, "error.html", {'error': 'Not enough records to update the second last entry.'})
            else:
                le= len(vechical_list)-2
                book = vechical_list[le]
                print('---------------------------')
                print(f"Bill ID: {book.bill_id}")
                print(f"Vehicle NO: {book.vehicle_no}")
                print(f"Buying Date: {book.buying_date}")
                print('--------------------------- km type and starting_KM', type(km) , type(book.starting_KM) )
                if book.starting_KM is not None:
                    if float(km) >float(book.starting_KM):
                        book.Ending_KM = km
                        book.Mileage = round((float(km)-float(book.starting_KM))/book.fuel_quantity,2)
                        book.proof_date = proof_date
                        book.save()
                        form.save()
                        print('--------------------------- km type and starting_KM', type(float(km)) , type(float(book.starting_KM)) )
                        print(f"Ending_KM: {book.Ending_KM}")
                        print(f"Mileage: {book.Mileage}")
                        return render(request, "data_upload.html", {'success': f"The Kilometer have been successfully update in the respative Bill ID","vechical": vechical})
                    else:
                        return render(request, "data_upload.html", {'error_message': f"Entered Kilometer Lesser than Starting km ,Ceck it and Enter again","vechical": vechical})
                else:
                    print("Error: Starting KM is None.")
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
        print('******************',vehicle_nos)
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
    p.setFont("Helvetica", 12)

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





def generate_pdf(request):
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pdf')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="your_file_name.pdf"'  # Open in a new tab
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pdf')
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    # transport_approval = get_object_or_404(transport_approval, bill_id=bill_id)
    # Add watermark text within the rectangle
    watermark_text = "Ramco Institute of Technology"
    p.setFont("Helvetica-Bold", 36)
    p.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray color for the watermark
    p.saveState()
    p.translate(300, 613)  # Translate to the center of the rectangle
    p.rotate(33)  # Rotate the text for the watermark effect
    p.drawCentredString(0, 0, watermark_text)
    p.restoreState()
    p.setFont("Helvetica-Bold", 36)
    # Title
    p.setFont("Helvetica-Bold", 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(170, height - 50, "P.A.C.R. SETHURAMAMMAL CHARITY TRUST")
    p.setFont("Helvetica", 10)
    p.drawString(230, height - 70, "BPCL, DEALERS @ 236463")
    p.drawString(180, height - 85, "P.A.C. RAMASAMY RAJASALAI, RAJAPALAYAM.")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, height - 30, "No:")
    p.setFont("Helvetica", 10)

    p.setFont("Helvetica-Bold", 10)
    p.drawString(380, height - 110, "Date&Time:")
    p.setFont("Helvetica", 10)

    # Car Details
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 110, "Please Supply for Car No:")
    p.setFont("Helvetica", 10)

    # Items
    p.setFont("Helvetica-Bold", 10)
    p.drawString(180, height - 140, "Fuel Type")
    p.drawString(260, height - 140, ":")

    p.drawString(180, height - 160, "Amount")
    p.drawString(260, height - 160, ":")

    p.drawString(180, height - 180, "Speed Petrol")
    p.drawString(260, height - 180, ":")

    p.drawString(180, height - 200, "Engine Oil")
    p.drawString(260, height - 200, ":")

    p.drawString(180, height - 220, "Grease")
    p.drawString(260, height - 220, ":")

    p.drawString(180, height - 240, "Distilled Water")
    p.drawString(260, height - 240, ":")

    # Signature and Address
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 300, "Transport Incharge")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(430, height - 300, "GM Admin")

    p.rect(50, 470, 500, 310)
   
    # Seal (simulated by drawing an ellipse and text)
    image_path = "image.jpg"  # Update with the correct path
    if os.path.isfile(image_path):
        img = Image.open(image_path)
        img_reader = ImageReader(img)
        p.drawImage(img_reader, 340, height - 320, width=70, height=70)  # Adjust the coordinates and size as needed

    p.showPage()
    p.save()

    return response