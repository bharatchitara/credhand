from django.conf import settings
import random


def calculate_brokerage(amount):
    """Calculate brokerage: 0.3% or 100 INR whichever is higher"""
    percentage_brokerage = amount * settings.BROKERAGE_PERCENTAGE
    return max(percentage_brokerage, settings.BROKERAGE_MINIMUM)


def generate_otp(length=6):
    """Generate random OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
