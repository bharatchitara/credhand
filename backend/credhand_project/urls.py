"""
URL configuration for credhand_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from authentication.views import (
    home_view, dashboard_view, card_lending_view, 
    transaction_history_view, payment_view, 
    payment_success_view, payment_failure_view, login_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('card_lending/', card_lending_view, name='card_lending'),
    path('transaction_history/', transaction_history_view, name='transaction_history'),
    path('payment/', payment_view, name='payment'),
    path('payment_success/', payment_success_view, name='payment_success'),
    path('payment_failure/', payment_failure_view, name='payment_failure'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('cards/', include('cards.urls')),
    path('transactions/', include('transactions.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
