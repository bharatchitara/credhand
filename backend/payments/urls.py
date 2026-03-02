from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('verify-signature/', views.verify_signature, name='verify_signature'),
    path('initiate/', views.initiate_payment, name='initiate'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('callback/', views.payment_callback, name='callback'),
    path('status/<int:payment_id>/', views.payment_status, name='status'),
]
