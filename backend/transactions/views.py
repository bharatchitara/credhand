from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from .models import Transaction, Refund, Investment
from cards.models import CreditCard
from .services import calculate_brokerage, calculate_charge_breakdown, create_card_details
from .utils import generate_otp
import logging

logger = logging.getLogger(__name__)


@login_required(login_url='authentication:login')
@require_http_methods(["POST"])
def calculate_charge(request):
    """Calculate service charge for a given amount with detailed breakdown"""
    try:
        data = json.loads(request.body)
        amount = float(data.get('amount', 0))
        
        # Validate amount
        if amount < 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Amount must be positive'
            }, status=400)
        
        # Calculate brokerage
        brokerage = calculate_brokerage(amount)
        breakdown = calculate_charge_breakdown(amount)
        total_amount = amount + brokerage
        
        return JsonResponse({
            'status': 'success',
            'amount': str(amount),
            'brokerage': str(brokerage),
            'total': str(total_amount),
            'breakdown': {
                'processing_fee': str(breakdown['processing_fee']),
                'risk_coverage': str(breakdown['risk_coverage']),
                'platform_fee': str(breakdown['platform_fee']),
            }
        })
    
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid amount format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error calculating charge: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to calculate charge'
        }, status=500)


@login_required(login_url='authentication:login')
@require_http_methods(["POST"])
def initiate_transaction(request):
    """Initiate a new transaction"""
    try:
        data = json.loads(request.body)
        card_id = data.get('card_id')
        purchase_type = data.get('purchase_type')
        amount = float(data.get('amount', 0))
        
        # Validate minimum amount
        if amount < 10:
            return JsonResponse({
                'status': 'error',
                'message': 'Minimum amount is 10 INR'
            }, status=400)
        
        # Validate maximum amount
        if amount > 100000:
            return JsonResponse({
                'status': 'error',
                'message': 'Maximum amount is 1 Lakh INR'
            }, status=400)
        
        # Get card
        try:
            card = CreditCard.objects.get(id=card_id, is_active=True)
        except CreditCard.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid card selected'
            }, status=400)
        
        # Calculate brokerage
        brokerage = calculate_brokerage(amount)
        total_amount = amount + brokerage
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=request.user,
            card=card,
            purchase_type=purchase_type,
            amount=amount,
            brokerage_amount=brokerage,
            total_amount=total_amount,
            status='pending'
        )
        
        return JsonResponse({
            'status': 'success',
            'transaction_id': transaction.id,
            'amount': str(amount),
            'brokerage': str(brokerage),
            'total_amount': str(total_amount),
            'card_name': card.card_name,
        })
    
    except Exception as e:
        logger.error(f"Error initiating transaction: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to initiate transaction'
        }, status=500)


@login_required(login_url='authentication:login')
@require_http_methods(["GET"])
def transaction_list(request):
    """Get list of user transactions"""
    transactions = Transaction.objects.filter(user=request.user).values(
        'id', 'purchase_type', 'amount', 'total_amount', 'status', 'created_at'
    )
    return JsonResponse({
        'status': 'success',
        'transactions': list(transactions)
    })


@login_required(login_url='authentication:login')
@require_http_methods(["GET"])
def transaction_detail(request, transaction_id):
    """Get transaction details"""
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        return JsonResponse({
            'status': 'success',
            'transaction': {
                'id': transaction.id,
                'card_name': transaction.card.card_name,
                'purchase_type': transaction.purchase_type,
                'amount': str(transaction.amount),
                'brokerage': str(transaction.brokerage_amount),
                'total_amount': str(transaction.total_amount),
                'status': transaction.status,
                'created_at': transaction.created_at.isoformat(),
            }
        })
    except Transaction.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Transaction not found'
        }, status=404)


@login_required(login_url='authentication:login')
@require_http_methods(["POST"])
def verify_payment(request):
    """Verify payment and check amount match"""
    try:
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        payment_amount = float(data.get('payment_amount', 0))
        
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        
        # Check if payment amount matches
        if payment_amount == float(transaction.total_amount):
            # Payment verified - update status
            transaction.status = 'payment_success'
            transaction.save()
            
            # Generate card details
            card_details = create_card_details()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Payment verified successfully',
                'card': card_details,
            })
        else:
            # Payment mismatch
            transaction.status = 'payment_failed'
            transaction.save()
            
            return JsonResponse({
                'status': 'mismatch',
                'message': 'Payment amount does not match',
                'expected': str(transaction.total_amount),
                'received': str(payment_amount),
                'options': [
                    {
                        'type': 'refund',
                        'label': 'Instant Refund',
                        'description': 'Refund the entire amount'
                    },
                    {
                        'type': 'invest',
                        'label': 'Invest Amount',
                        'description': 'Invest at 1% monthly return'
                    }
                ]
            })
    
    except Transaction.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Transaction not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to verify payment'
        }, status=500)
