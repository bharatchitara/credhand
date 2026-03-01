from django.contrib import admin
from .models import Transaction, Refund, Investment


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card', 'amount', 'status', 'created_at')
    list_filter = ('status', 'purchase_type', 'created_at')
    search_fields = ('user__email', 'id')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'status', 'monthly_return', 'created_at')
    list_filter = ('status',)
