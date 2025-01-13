import stripe
from core.settings import settings
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.fulfillment_service import get_fulfillment_service

stripe.api_key = settings.stripe_api_key

webhook_router = APIRouter()
payment_tags_metadata = {"name": "", "description": ""}


@webhook_router.post("/webhook")
async def my_webhook_view(request: Request):
    fulfillment_service = get_fulfillment_service()
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.webhook_secret
        )

    except ValueError:
        return JSONResponse(content={"status": "Invalid payload"}, status_code=400)
    except stripe.error.SignatureVerificationError:
        return JSONResponse(content={"status": "Invalid signature"}, status_code=400)

    if (
        event['type'] == 'checkout.session.completed'
        or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfillment_service.fulfill_checkout(event['data']['object']['id'])

    return JSONResponse(content={"status": "success"}, status_code=200)
