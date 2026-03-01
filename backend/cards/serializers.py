from rest_framework import serializers
from .models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'card_name', 'card_issuer', 'features', 'available_limit']
