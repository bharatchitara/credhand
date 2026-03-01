from django.db import models
from django.conf import settings
from cards.models import CreditCard


class Transaction(models.Model):
    """Transaction Model - User requesting credit card limit"""
    PURCHASE_TYPES = [
        ('flight', 'Flight Booking'),
        ('shopping', 'Online Shopping'),
        ('ecomm', 'E-Commerce'),
        ('bills', 'Bills'),
        ('rent', 'Rent'),
        ('others', 'Others'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('payment_initiated', 'Payment Initiated'),
        ('payment_success', 'Payment Successful'),
        ('payment_failed', 'Payment Failed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(CreditCard, on_delete=models.PROTECT)
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    brokerage_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    card_last_four = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaction {self.id} - {self.user.email}"

    def calculate_brokerage(self):
        """Calculate brokerage: 0.3% or 100 INR whichever is higher"""
        percentage_brokerage = self.amount * 0.003  # 0.3%
        return max(percentage_brokerage, 100)


class Refund(models.Model):
    """Refund Model - For refunding payment if amount mismatch"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='refund')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'

    def __str__(self):
        return f"Refund for Transaction {self.transaction.id}"


class Investment(models.Model):
    """Investment Model - For investing payment amount at 1% monthly return"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='investment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_return = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    maturity_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'

    def __str__(self):
        return f"Investment for Transaction {self.transaction.id}"

    def calculate_monthly_return(self):
        """Calculate 1% monthly return"""
        return self.amount * 0.01
