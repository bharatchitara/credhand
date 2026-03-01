from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('list/', views.card_list, name='list'),
    path('detail/<int:card_id>/', views.card_detail, name='detail'),
]
