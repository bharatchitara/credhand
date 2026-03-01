from django.contrib import admin
from .models import Payment, OTP


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'amount_paid', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('upi_ref', 'transaction__id')


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
