import random
from datetime import datetime, timedelta


def calculate_brokerage(amount):
    """
    Calculate brokerage as a flat 5% of the requested amount.
    
    Returns: brokerage_amount (float)
    """
    return round((amount * 5) / 100, 2)


def calculate_charge_breakdown(amount):
    """
    Calculate and return detailed charge breakdown for transparency.
    Shows how the service charge is composed.
    
    Returns: {
        'processing_fee': amount,
        'risk_coverage': amount,
        'platform_fee': amount,
        'total': amount
    }
    """
    brokerage = calculate_brokerage(amount)
    
    # Breakdown percentages that sum to 100%
    processing_pct = 50      # 50% for processing infrastructure
    risk_pct = 30            # 30% for risk/fraud coverage
    platform_pct = 20        # 20% for platform maintenance
    
    breakdown = {
        'processing_fee': round((brokerage * processing_pct) / 100, 2),
        'risk_coverage': round((brokerage * risk_pct) / 100, 2),
        'platform_fee': round((brokerage * platform_pct) / 100, 2),
        'total': brokerage,
    }
    
    # Ensure total matches due to rounding
    total_breakdown = (
        breakdown['processing_fee'] + 
        breakdown['risk_coverage'] + 
        breakdown['platform_fee']
    )
    if total_breakdown != brokerage:
        breakdown['platform_fee'] = round(brokerage - breakdown['processing_fee'] - breakdown['risk_coverage'], 2)
    
    return breakdown


def create_card_details():
    """Create mock credit card details for lending"""
    # In production, this would fetch actual card details from a secure vault
    card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    expiry_month = random.randint(1, 12)
    expiry_year = datetime.now().year + random.randint(2, 5)
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    return {
        'card_number': card_number,
        'expiry': f"{expiry_month:02d}/{expiry_year}",
        'cvv': cvv,
        'cardholder_name': 'CREDHAND USER',
    }


def process_refund(transaction):
    """Process refund for transaction"""
    from .models import Refund
    
    refund = Refund.objects.create(
        transaction=transaction,
        amount=transaction.total_amount,
        reason='Payment amount mismatch - User requested refund'
    )
    return refund


def process_investment(transaction):
    """Process investment for transaction"""
    from .models import Investment
    
    monthly_return = transaction.total_amount * 0.01
    maturity_date = datetime.now() + timedelta(days=30)
    
    investment = Investment.objects.create(
        transaction=transaction,
        amount=transaction.total_amount,
        monthly_return=monthly_return,
        maturity_date=maturity_date
    )
    return investment
