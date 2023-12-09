import stripe
from django.urls import reverse
from rest_framework.response import Response

from config import settings


def perform_payment(amount):
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_payment = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        payment_method="pm_card_visa",
    )

    stripe.PaymentIntent.confirm(
        stripe_payment['id'],
        payment_method="pm_card_visa",
        return_url="https://www.google.com/",
    )

    return stripe_payment


def get_payment(stripe_id):
    stripe.api_key = settings.STRIPE_API_KEY
    payment_intent = stripe.PaymentIntent.retrieve(stripe_id)
    return Response({
        'status': payment_intent.status, })

