import stripe
from core.settings import settings
from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from services.validation import check_roles

stripe.api_key = settings.stripe_api_key

payment_router = APIRouter()
payment_tags_metadata = {"name": "", "description": ""}


@payment_router.get(
    "/subscription",
    summary="",
    description="",
    response_description="",
)
async def pay(user_id: str, check_roles: bool = Depends(check_roles)):
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
            metadata={
                'user_id': user_id,
            },
        )
    except stripe.error.StripeError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)


@payment_router.get(
    "/subscription_with_sale",
    summary="",
    description="",
    response_description="",
)
async def sale(user_id: str, coupon: str = "B56Tx9DM", check_roles: bool = Depends(check_roles)):
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
            metadata={
                'user_id': user_id,
            },
        )
    except stripe.error.StripeError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)




@payment_router.get(
    "/trial",
    summary="",
    description="",
    response_description="",
)
async def trial(user_id: str, check_roles: bool = Depends(check_roles)):
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
            metadata={
                'user_id': user_id,
            },
        )
    except stripe.error.StripeError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})

    return RedirectResponse(checkout_session.url, status_code=status.HTTP_302_FOUND)




@payment_router.post(
    "/refund"
)
async def refund(payment_id: str, check_roles: bool = Depends(check_roles)) -> HTMLResponse:
    try:
        stripe.Refund.create(payment_intent=payment_id)
        return HTMLResponse(status_code=200)
    except stripe.error.StripeError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})



@payment_router.post(
    "/cancel"
)
async def cancel_subscription(subscription_id: str, check_roles: bool = Depends(check_roles)):
    try:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True,
        )
        return HTMLResponse(status_code=200)
    except stripe.error.StripeError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})