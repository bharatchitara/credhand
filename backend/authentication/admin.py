from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('OAuth Info', {'fields': ('oauth_id', 'oauth_provider')}),
        ('KYC', {'fields': ('kyc_status', 'phone')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'oauth_provider', 'kyc_status')
