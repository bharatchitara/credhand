from django.db import models


class CreditCard(models.Model):
    """Credit Card Model"""
    card_name = models.CharField(max_length=100)
    card_issuer = models.CharField(
        max_length=50,
        choices=[
            ('hdfc', 'HDFC'),
            ('icici', 'ICICI'),
            ('axis', 'Axis'),
            ('sbi', 'SBI'),
            ('yes', 'Yes Bank'),
            ('kotak', 'Kotak'),
            ('amex', 'American Express'),
        ]
    )
    features = models.TextField(help_text="Features of the credit card, comma separated")
    available_limit = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Credit Card'
        verbose_name_plural = 'Credit Cards'
        ordering = ['card_issuer', 'card_name']

    def __str__(self):
        return f"{self.card_name} - {self.card_issuer.upper()}"
