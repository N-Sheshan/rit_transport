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
from django.urls import path, include
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout_view, name="logout"),
    # path('register/', views.register, name='register'),
    path('fuel_application/', views.fuel_application, name="fuel_application"),
    path('fuel_application_PS/', views.fuel_application_PS, name="fuel_application_PS"),
    path('data_update', views.data_update, name="data_update"),
    path('history', views.history, name="history"),
    path('ps_history', views.ps_history, name="ps_history"),
    path('new_vechical', views.new_vechical, name="new_vechical"),
    path('generate_pdf/<path:f_type>/<path:bill_id>',views.generate_pdf, name='generate_pdf'),
    path('get_bills/<str:vehicle_no>/', views.get_bills_for_vehicle, name='get_bills'),
    path('scan/', views.qr_scanner, name='qr_scanner'),

]
