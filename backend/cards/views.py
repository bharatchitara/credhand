from django.http import JsonResponse
from .models import CreditCard


def card_list(request):
    """Get list of all active credit cards"""
    cards = CreditCard.objects.filter(is_active=True).values(
        'id', 'card_name', 'card_issuer', 'features', 'available_limit'
    )
    return JsonResponse({
        'status': 'success',
        'cards': list(cards)
    })


def card_detail(request, card_id):
    """Get details of a specific card"""
    try:
        card = CreditCard.objects.get(id=card_id, is_active=True)
        return JsonResponse({
            'status': 'success',
            'card': {
                'id': card.id,
                'card_name': card.card_name,
                'card_issuer': card.card_issuer,
                'features': card.features,
                'available_limit': str(card.available_limit),
            }
        })
    except CreditCard.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Card not found'
        }, status=404)
