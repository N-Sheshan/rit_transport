from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import pandas as pd
from application.form import fuel_bill_detials,KM_update
from application.models import transport_approval
# Create your views here.


def fuel_application(request):
    excel_file_path = 'category.csv'
    # Read the Excel file
    try:
        df = pd.read_csv(excel_file_path)
    except pd.errors.EmptyDataError:
        # Handle the case where the Excel file is empty
        df = pd.DataFrame(columns=['Sub_category'])
    category = df['Sub_category'].tolist()
    current_year = datetime.now().year
    current_month = datetime.now().strftime('%m')
    if request.method == 'POST':
        form = fuel_bill_detials(request.POST)
        if form.is_valid():
            data = transport_approval.objects.filter(buying_date__year=current_year, buying_date__month=current_month)
            count = data.count()
            user=form.save(commit=False)
            user.bill_id=str(current_year)+str(current_month)+f'{count+1:03d}'
            user.vechical_type = '4 whell'
            user.fule_type = 'petrol'
            user.route = 'rajaplayam'
            user.save()
            return render(request, "index.html",{"category":category})
        else:
            return render(request, "error.html", {'form': form})
    
    return render(request, "index.html",{"category":category})

def data_update(request):
    if request.method == 'POST':
        # Retrieve the existing instance based on bill_id from the POST data
        bill_id = request.POST.get('bill_id')
        book = get_object_or_404(transport_approval, bill_id=bill_id)

        # Create the form with the existing instance
        form = KM_update(request.POST, instance=book)
        
        if form.is_valid():
            form.save()
            return render(request, "data_upload.html", {'form': form})
        else:
            # Print form errors for debugging
            print(form.errors)
            return render(request, "error.html", {'form': form})
    else:
        form = KM_update()
    
    return render(request, "data_upload.html", {'form': form})


def history(request):
    excel_file_path = 'category.csv'
    # Read the Excel file
    try:
        df = pd.read_csv(excel_file_path)
    except pd.errors.EmptyDataError:
        # Handle the case where the Excel file is empty
        df = pd.DataFrame(columns=['Sub_category'])
    category = df['Sub_category'].tolist()
    if request.method == 'POST':
        vechical_no = request.POST.get('vechical_no')
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        print('---------------------------------',vechical_no,from_date_str,to_date_str)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        # Filter based on vechical_no and date range
        if vechical_no == None :
            filtered_transport_approvals = transport_approval.objects.filter(
            buying_date__range=[from_date, to_date] )
        else:
            filtered_transport_approvals = transport_approval.objects.filter(
            vechical_no=vechical_no,
            buying_date__range=[from_date, to_date] )
        if filtered_transport_approvals:
            return render(request, 'history.html', {'data': filtered_transport_approvals,"category":category})
    
    return render(request, "history.html",{"category":category})

    # views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    # transport_approval = get_object_or_404(transport_approval, bill_id=bill_id)

    # Title
    p.setFont("Helvetica-Bold", 12)
    p.drawString(150, height - 50, "P.A.C.R. SETHURAMAMMAL CHARITY TRUST")
    p.setFont("Helvetica", 10)
    p.drawString(210, height - 70, "BPCL, DEALERS @ 236463")
    p.drawString(150, height - 85, "P.A.C. RAMASAMY RAJASALAI, RAJAPALAYAM.")

    # Bill Number and Date
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 30, "To:")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, height - 30, "No:")
    p.setFont("Helvetica", 10)
    # p.drawString(430, height - 30, transport_approval.bill_id )

    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, height - 110, "Date:")
    p.setFont("Helvetica", 10)
    # p.drawString(430, height - 110, transport_approval.buying_date)

    # Car Details
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 110, "Please Supply for Car No:")
    p.setFont("Helvetica", 10)
    # p.drawString(230, height - 110, transport_approval.vechical_no)

    # Items
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 140, "Fuel Type")
    # p.drawString(250, height - 140, transport_approval.fule_type)
    p.drawString(350, height - 140, "")

    p.drawString(100, height - 160, "Amount")
    # p.drawString(250, height - 160, transport_approval.fuel_amount)

    p.drawString(100, height - 180, "Speed Petrol")
    p.drawString(250, height - 180, "Litres")
    p.drawString(350, height - 180, "")

    p.drawString(100, height - 200, "Engine Oil")
    p.drawString(250, height - 200, "K.G.")
    p.drawString(350, height - 200, "")

    p.drawString(100, height - 220, "Grease")
    p.drawString(250, height - 220, "K.G.")
    p.drawString(350, height - 220, "")

    p.drawString(100, height - 240, "Distilled Water")
    p.drawString(250, height - 240, "Bottles")
    p.drawString(350, height - 240, "")

    # Signature and Address
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 280, "Signature")
    p.line(200, 785, 250, 785)

    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, height - 300, "Address")
    p.setFont("Helvetica", 10)
    p.drawString(200, height - 300, "Transport Incharge")
    p.line(200, 805, 250, 805)

    # Seal (simulated by drawing an ellipse and text)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(350, height - 270, "R.I.T.")
    p.ellipse(330, height - 290, 420, height - 250)

    p.showPage()
    p.save()

    return response

