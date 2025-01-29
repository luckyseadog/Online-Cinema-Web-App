import logging
from functools import lru_cache

import stripe
from core.settings import settings
from db.redis_db import get_redis

logging.basicConfig(
    level=logging.DEBUG,
)

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = settings.stripe_api_key


class FulfillmentService:
    def __init__(self):
        self._redis = get_redis()

    async def fulfill_checkout(self, session_id, metadata):
        print("Fulfilling Checkout Session", session_id)

        # TODO: Make this function safe to run multiple times,
        # even concurrently, with the same session ID

        # TODO: Make sure fulfillment hasn't already been
        # peformed for this Checkout Session

        if not await self._redis.set(f'fulfill_checkout:{session_id}', "in process", nx=True):
            return

        # Retrieve the Checkout Session from the API with line_items expanded
        checkout_session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['line_items'],
        )
        
        subscription_id = checkout_session.subscription
        subscription = stripe.Subscription.retrieve(subscription_id)
        invoice = stripe.Invoice.retrieve(subscription.latest_invoice)
        payment_intent_id = invoice.payment_intent

        customer = checkout_session.customer
        customer_info = stripe.Customer.retrieve(customer)

        user_id = metadata.get("user_id")

        # Check the Checkout Session's payment_status property
        # to determine if fulfillment should be peformed
        if checkout_session.payment_status != 'unpaid':
            # TODO: Perform fulfillment of the line items

            # TODO: Record/save fulfillment status for this
            # Checkout Session
            logging.debug("============OPERATION INFO============")
            logging.debug(f"User Internal ID: {user_id}")
            logging.debug(f"Payment Intent ID: {payment_intent_id}")

            for item in checkout_session.line_items.data:
                logging.debug(f"Product: {item.description}, Quantity: {item.quantity}, Price: {item.amount_total / 100} {checkout_session.currency.upper()}")

            logging.debug(f"Customer Email: {customer_info.email}")
            logging.debug(f"Customer Name: {customer_info.name}")

            self._redis.set(f'fulfill_checkout:{session_id}', "done")
            # TODO: Make worker that checks that there is no "in process"


@lru_cache
def get_fulfillment_service() -> FulfillmentService:
    return FulfillmentService()
