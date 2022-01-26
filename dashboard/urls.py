from django.urls import path

from . import views

urlpatterns = [
    path('info', views.info, name='info'),
    path('maintenance', views.maintenance, name='maintenance'),
    path('maintenance_redirect', views.maintenance_redirect, name = 'maintenance_redirect'),
    path('floorplans', views.floorplans, name='floorplans'),
    path('gallery', views.gallery, name='gallery'),
    path('amenities', views.amenities, name='amenities'),
    path('FAQ', views.faq, name='FAQ'),
    path('pay', views.pay, name='pay'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('reslogin', views.reslogin, name='reslogin'),
    path('employeelogin', views.employeelogin, name = 'employeelogin'),
    path('resident_register', views.resident_register, name = 'resident_register'),
    path('employee_register', views.employee_register, name = 'employee_register'),
    path('important_numbers', views.important_numbers, name = 'important_numbers'),
    path('', views.index, name='index'),
    path('userpage/', views.userpage, name='userpage'),
    path('employeepage', views.employeepage, name='employeepage'),
    path('applyForApartment', views.applyForApartment, name = 'applyForApartment'),
    path('saveRow', views.saveRow, name = 'saveRow'),
    path('amenities_redirect', views.amenities_redirect, name='amenities_redirect'),
    path('amenities_slot', views.amenities_slot, name='amenities_slot'),
    path('Documents', views.Documents, name = 'Documents'),
    path('documentsUpload', views.documentsUpload, name = 'documentsUpload'),
    path('paymentInfo', views.paymentInfo, name = 'paymentInfo'),
    path('payment_redirect', views.payment_redirect, name='payment_redirect'),
]