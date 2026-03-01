from django.contrib import admin
from .models import CreditCard


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'card_issuer', 'available_limit', 'is_active')
    list_filter = ('card_issuer', 'is_active')
    search_fields = ('card_name', 'card_issuer')
