from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import pandas as pd
from application.form import fuel_bill_detials,KM_update
from application.models import transport_approval,Master_Vechicle
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
    category = Master_Vechicle.objects.all()
    current_year = datetime.now().year
    current_month = datetime.now().strftime('%m')
    
    if request.method == 'POST':
        form = fuel_bill_detials(request.POST)
        if form.is_valid():
            vehicle_no = form.cleaned_data['vehicle_no']
            data = transport_approval.objects.filter(buying_date__year=current_year, buying_date__month=current_month)
            master_data = Master_Vechicle.objects.filter(vehicle_no=vehicle_no).first()  # Get the first instance or None
            
            if master_data and form.cleaned_data['status'] == "Yes":
                count = data.count()
                user = form.save(commit=False)
                user.bill_id = 'RIT'+str(current_year) + str(current_month) + f'{count + 1:03d}'
                user.vehicle_type = master_data.vehicle_type
                user.fule_type = master_data.fule_type
                user.route = master_data.route_name
                user.save()
                generate_pdf(request)
                # return redirect(reverse('generate_pdf_view', kwargs={'bill_id': user.bill_id}))  
                return render(request, "index.html", {"category": category, "success": "Bill details have been successfully submitted."})
            else:
                return render(request, "index.html", {"category": category, 'error_message': 'Vehicle not found or approval not given'})
        else:
            return render(request, "error.html", {'form': form})
    
    return render(request, "index.html", {"category": category})

def data_update(request):
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        km =  request.POST.get('starting_KM')
        proof_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vechical_filter = get_object_or_404(transport_approval, bill_id=bill_id)
        vehicle_no = vechical_filter.vehicle_no
        date = vechical_filter.buying_date
        # print('+++++++++++++++++',vehicle_no)
        if vechical_filter.starting_KM is None:
            vechical_list = transport_approval.objects.filter(vehicle_no=vehicle_no, buying_date__lte=date).order_by('buying_date')
            # for s in vechical_list:
            #     print('#######',s.bill_id,'->',s.buying_date)
            form = KM_update(request.POST, instance=vechical_filter)
            if len(vechical_list) < 2:
                if form.is_valid():
                    form.save()
                    return render(request, "data_upload.html", {'form': form})
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
                # print('--------------------------- km type and starting_KM', type(km) , type(book.starting_KM) )
                if book.starting_KM is not None:
                    if float(km) >float(book.starting_KM):
                        book.Ending_KM = km
                        book.Mileage = round((float(km)-float(book.starting_KM))/book.fuel_quantity,2)
                        book.proof_date = proof_date
                        book.save()
                        form.save()
                        # print('--------------------------- km type and starting_KM', type(float(km)) , type(float(book.starting_KM)) )
                        # print(f"Ending_KM: {book.Ending_KM}")
                        # print(f"Mileage: {book.Mileage}")
                        return render(request, "data_upload.html", {'success': f"The Kilometer have been successfully update in the respative Bill ID"})
                    else:
                        return render(request, "data_upload.html", {'error_message': f"Entered Kilometer Lesser than Starting km ,Ceck it and Enter again"})
                else:
                    print("Error: Starting KM is None.")
                    return render(request, "data_upload.html", {'error_message': f"Starting KM is None."})
        else:
            return render(request, "data_upload.html", {'error_message': f"Kilometer already exists for this {bill_id} Bill ID, so data upload is not allowed"})
    else:
        form = KM_update()
    
    return render(request, "data_upload.html", {'form': form})


def history(request):
    category = Master_Vechicle.objects.all()
    filtered_transport_approvals = transport_approval.objects.all()
    if request.method == 'POST':
        vehicle_no = request.POST.get('vehicle_no')
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        # print('---------------------------------',vehicle_no,from_date_str,to_date_str)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        # Filter based on vehicle_no and date range
        if vehicle_no == None :
            filtered_transport_approvals = transport_approval.objects.filter(
            buying_date__range=[from_date, to_date] )
        else:
            filtered_transport_approvals = transport_approval.objects.filter(
            vehicle_no=vehicle_no,
            buying_date__range=[from_date, to_date] )
        if filtered_transport_approvals:
            return render(request, 'history.html', {'data': filtered_transport_approvals,"category":category})
    download_format = request.GET.get('download', None)
    if download_format == 'excel':
        # Generate Excel file
        workbook = Workbook()
        worksheet = workbook.active
        # Add headers
        headers = ["bill_id", "vehicle_no", "driver_id", "vehicle_type", "fule_type", 
                   "buying_date", "reason", "fuel_quantity", "route", 
                   "starting_KM", "Ending_KM", "Mileage", "status"]
        worksheet.append(headers)
        # Add data
        for item in filtered_transport_approvals:
            row_data = [getattr(item, field) for field in headers]
            worksheet.append(row_data)
        # Prepare response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="transport_report.xlsx"'
        workbook.save(response)
        return response

    elif download_format == 'pdf':
         # Generate PDF file
        template = 'history.html'  # Separate template for just the table
        context = {'data': filtered_transport_approvals}
        html = render_to_string(template, context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transport_report.pdf"'
        
        # Optimize PDF generation
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
        }
        pdf = pdfkit.from_string(html, False, options=options)
        
        response.write(pdf)
        return response
    return render(request, "history.html",{'data': filtered_transport_approvals,"category":category})



def export_to_excel(request):
    print('---------------export_to_excel')
    # Query your data
    data = transport_approval.objects.all().values('bill_id', 'vehicle_no', 'driver_id', 'vehicle_type', 'fuel_type', 'buying_date', 'reason', 'fuel_quantity', 'route', 'starting_KM', 'Ending_KM', 'Mileage', 'status')

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create a HttpResponse object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="table_data.xlsx"'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    return response


def generate_pdf(request):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pdf')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="your_file_name.pdf"'  # Open in a new tab
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pdf')
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