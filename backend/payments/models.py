from django.db import models
from transactions.models import Transaction


class Payment(models.Model):
    """Payment Model - UPI payment tracking"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('otp_sent', 'OTP Sent'),
        ('otp_verified', 'OTP Verified'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='payment')
    upi_ref = models.CharField(max_length=255, unique=True, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, default='upi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Transaction {self.transaction.id}"


class OTP(models.Model):
    """OTP Model - For payment verification"""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='otp')
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return f"OTP for Payment {self.payment.id}"

    def is_expired(self):
        """Check if OTP has expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def verify_otp(self, entered_otp):
        """Verify entered OTP"""
        if self.is_expired():
            return False, "OTP expired"
        
        if self.attempts >= self.max_attempts:
            return False, "Maximum attempts exceeded"
        
        self.attempts += 1
        self.save()
        
        if str(entered_otp) == str(self.otp_code):
            self.is_verified = True
            self.save()
            return True, "OTP verified successfully"
        
        return False, f"Invalid OTP. Attempts remaining: {self.max_attempts - self.attempts}"
