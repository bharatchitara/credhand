from django.conf import settings
import uuid
import logging

logger = logging.getLogger(__name__)


def initiate_upi_payment(transaction, payment):
    """
    Initiate UPI payment with payment gateway
    
    Supports: Razorpay, PhonePe
    """
    gateway = settings.UPI_GATEWAY
    
    # Generate unique reference
    upi_ref = f"CREDHAND_{transaction.id}_{uuid.uuid4().hex[:8]}".upper()
    
    if gateway == 'razorpay':
        return initiate_razorpay_payment(transaction, payment, upi_ref)
    elif gateway == 'phonepe':
        return initiate_phonepe_payment(transaction, payment, upi_ref)
    else:
        raise ValueError(f"Unsupported payment gateway: {gateway}")


def initiate_razorpay_payment(transaction, payment, upi_ref):
    """Initialize Razorpay UPI payment"""
    try:
        import razorpay
        
        client = razorpay.Client(
            auth=(settings.UPI_KEY_ID, settings.UPI_KEY_SECRET)
        )
        
        # Create order
        order_data = {
            "amount": int(transaction.total_amount * 100),  # Amount in paise
            "currency": "INR",
            "receipt": upi_ref,
            "payment_capture": 1
        }
        
        order = client.order.create(data=order_data)
        return order['id']
    
    except Exception as e:
        logger.error(f"Error initiating Razorpay payment: {str(e)}")
        raise


def initiate_phonepe_payment(transaction, payment, upi_ref):
    """Initialize PhonePe UPI payment"""
    try:
        import requests
        
        phonepe_endpoint = "https://api.phonepe.com/apis/hermes/initiatePayment"
        
        payload = {
            "merchantId": settings.UPI_KEY_ID,
            "merchantTransactionId": upi_ref,
            "merchantUserId": str(transaction.user.id),
            "amount": int(transaction.total_amount * 100),
            "redirectUrl": "http://localhost:8000/payments/callback/",
            "redirectMode": "POST",
            "callbackUrl": "http://localhost:8000/payments/callback/",
            "mobileNumber": transaction.user.phone or "9999999999",
            "paymentInstrument": {
                "type": "UPI",
                "targetApp": "PHONEPE"
            }
        }
        
        # Note: In production, you need to add proper encryption and signature
        response = requests.post(phonepe_endpoint, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('transactionId', upi_ref)
        else:
            raise Exception(f"PhonePe API error: {response.text}")
    
    except Exception as e:
        logger.error(f"Error initiating PhonePe payment: {str(e)}")
        raise


def process_payment_callback(callback_data):
    """Process payment gateway callback"""
    try:
        # Extract relevant data from callback
        upi_ref = callback_data.get('merchantTransactionId') or callback_data.get('receipt')
        payment_status = callback_data.get('status') or callback_data.get('state')
        
        from .models import Payment
        
        payment = Payment.objects.get(upi_ref=upi_ref)
        
        if payment_status in ['completed', 'COMPLETED', 'SUCCESS']:
            payment.payment_status = 'completed'
        else:
            payment.payment_status = 'failed'
        
        payment.save()
        return True
    
    except Exception as e:
        logger.error(f"Error processing payment callback: {str(e)}")
        return False
