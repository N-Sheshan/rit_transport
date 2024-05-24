"""
URL configuration for rit_transport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #type:ignore
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.fuel_application, name="fuel_application"),
    path('data_update', views.data_update, name="data_update"),
    path('history', views.history, name="history"),
    path('generate_pdf',views.generate_pdf, name='generate_pdf'),
    path('export_to_excel',views.export_to_excel, name='export_to_excel'),
]
