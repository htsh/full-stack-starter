import stripe
from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth import current_active_user
from app.config import settings
from app.models.user import User
from app.schemas.payment import CheckoutRequest, CheckoutResponse
from app.services.stripe import create_checkout_session, handle_checkout_completed

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout", response_model=CheckoutResponse)
async def checkout(
    body: CheckoutRequest,
    user: User = Depends(current_active_user),
):
    try:
        url = await create_checkout_session(user, body.package_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CheckoutResponse(checkout_url=url)


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        await handle_checkout_completed(event["data"]["object"])

    return {"status": "ok"}
