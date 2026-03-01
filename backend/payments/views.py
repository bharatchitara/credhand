from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import json
import logging
from .models import Payment, OTP
from transactions.models import Transaction
from .services import initiate_upi_payment, process_payment_callback
from .utils import generate_otp

logger = logging.getLogger(__name__)


@login_required(login_url='authentication:login')
@require_http_methods(["POST"])
def initiate_payment(request):
    """Initiate UPI payment"""
    try:
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        
        # Get transaction
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        
        # Create payment
        payment = Payment.objects.create(
            transaction=transaction,
            amount_paid=transaction.total_amount,
            payment_status='initiated'
        )
        
        # Initiate UPI payment
        upi_ref = initiate_upi_payment(transaction, payment)
        payment.upi_ref = upi_ref
        payment.payment_status = 'otp_sent'
        payment.save()
        
        # Generate and save OTP
        otp_code = generate_otp()
        otp_expires = timezone.now() + timedelta(minutes=5)
        
        otp = OTP.objects.create(
            payment=payment,
            otp_code=otp_code,
            expires_at=otp_expires
        )
        
        # In production, send OTP via SMS/Email
        # For now, we'll return it in response (NOT safe for production)
        
        return JsonResponse({
            'status': 'success',
            'payment_id': payment.id,
            'upi_ref': upi_ref,
            'message': 'OTP sent to your registered phone',
            'otp': otp_code,  # Remove in production
        })
    
    except Transaction.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Transaction not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error initiating payment: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to initiate payment'
        }, status=500)


@login_required(login_url='authentication:login')
@require_http_methods(["POST"])
def verify_otp(request):
    """Verify OTP for payment"""
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        entered_otp = data.get('otp')
        
        payment = Payment.objects.get(id=payment_id)
        
        # Verify OTP
        otp = payment.otp
        is_valid, message = otp.verify_otp(entered_otp)
        
        if not is_valid:
            return JsonResponse({
                'status': 'error',
                'message': message
            }, status=400)
        
        # Update payment status
        payment.payment_status = 'otp_verified'
        payment.save()
        
        # Update transaction status
        payment.transaction.status = 'payment_success'
        payment.transaction.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Payment verified successfully',
            'payment_id': payment.id,
        })
    
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Payment not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to verify OTP'
        }, status=500)


@require_http_methods(["POST"])
def payment_callback(request):
    """Handle payment gateway callback"""
    try:
        data = json.loads(request.body)
        
        # Process callback
        success = process_payment_callback(data)
        
        if success:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'}, status=400)
    
    except Exception as e:
        logger.error(f"Error processing payment callback: {str(e)}")
        return JsonResponse({'status': 'error'}, status=500)


@login_required(login_url='authentication:login')
@require_http_methods(["GET"])
def payment_status(request, payment_id):
    """Get payment status"""
    try:
        payment = Payment.objects.get(id=payment_id)
        
        return JsonResponse({
            'status': 'success',
            'payment': {
                'id': payment.id,
                'payment_status': payment.payment_status,
                'amount': str(payment.amount_paid),
                'created_at': payment.created_at.isoformat(),
            }
        })
    
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Payment not found'
        }, status=404)
