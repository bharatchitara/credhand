from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('initiate/', views.initiate_transaction, name='initiate'),
    path('list/', views.transaction_list, name='list'),
    path('detail/<int:transaction_id>/', views.transaction_detail, name='detail'),
    path('verify/', views.verify_payment, name='verify'),
    path('calculate-charge/', views.calculate_charge, name='calculate_charge'),
]
