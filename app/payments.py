import stripe
from config import STRIPE_API_KEY, COINBASE_API_KEY
from coinbase_commerce.client import Client as CoinbaseClient

stripe.api_key = STRIPE_API_KEY

def create_stripe_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Abonnement Premium ArchimindAI',
                    },
                    'unit_amount': 5000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success',
            cancel_url='https://yourdomain.com/cancel',
        )
        return session.url
    except Exception as e:
        print(f"Erreur lors de la création de la session Stripe : {e}")
        return "Erreur lors de la création de la session Stripe."

def create_coinbase_charge():
    try:
        client = CoinbaseClient(api_key=COINBASE_API_KEY)
        charge_data = {
            "name": "Abonnement Premium ArchimindAI",
            "description": "Paiement pour abonnement premium",
            "local_price": {
                "amount": "50.00",
                "currency": "USD"
            },
            "pricing_type": "fixed_price"
        }
        charge = client.charge.create(**charge_data)
        return charge.hosted_url
    except Exception as e:
        print(f"Erreur lors de la création de la charge Coinbase : {e}")
        return "Erreur lors de la création de la charge Coinbase."
