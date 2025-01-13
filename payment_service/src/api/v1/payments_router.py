from core.settings import settings
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader
from services.fulfillment_service import get_fulfillment_service

router = APIRouter()
payment_tags_metadata = {"name": "", "description": ""}


import stripe

stripe.api_key = settings.stripe_api_key


@router.get(
    "/subscription",
    summary="",
    description="",
    response_description="",
    tags=[""],
)
async def pay():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Qfuc3E1UjG6eS2xAvYlqj20',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=settings.success_url,
            cancel_url=settings.cancel_url + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)


@router.get(
    "/subscription_with_sale",
    summary="",
    description="",
    response_description="",
    tags=[""],
)
async def pay(coupon: str = "B56Tx9DM"):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Qfuc3E1UjG6eS2xAvYlqj20',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            discounts=[{
                'coupon': coupon,
            }],
            success_url=settings.success_url,
            cancel_url=settings.cancel_url + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)




@router.get(
    "/trial",
    summary="",
    description="",
    response_description="",
    tags=[""],
)
async def trial():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Qfuc3E1UjG6eS2xAvYlqj20',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            subscription_data={
                'trial_period_days': 30,
            },
            success_url=settings.success_url,
            cancel_url=settings.cancel_url + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)


@router.post("/webhook")
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


@router.post(
    "/refund"
)
async def refund(payment_id: str) -> HTMLResponse:
    stripe.Refund.create(payment_intent=payment_id)
    return HTMLResponse(status_code=200)



@router.post(
    "/cancel"
)
async def concel_subscription(subscription_id: str):
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True,
    )
    return HTMLResponse(status_code=200)

@router.get(
    "/success_response"
)
async def success():
    jinja_env = Environment(loader=FileSystemLoader("src/templates/"), autoescape=True)
    template = jinja_env.get_template("success.html")
    html_content = template.render()
    return HTMLResponse(content=html_content, status_code=200)


@router.get(
    "/cancel_response"
)
async def cancel():
    jinja_env = Environment(loader=FileSystemLoader("src/templates/"), autoescape=True)
    template = jinja_env.get_template("cancel.html")
    html_content = template.render()
    return HTMLResponse(content=html_content, status_code=200)
