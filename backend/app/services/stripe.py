import stripe

from app.config import settings
from app.models.user import User
from app.models.payment import Payment
from app.services.credits import add_credits

stripe.api_key = settings.stripe_secret_key

CREDIT_PACKAGES = {
    "starter": {"name": "Starter Pack", "credits": 50, "price_cents": 499},
    "pro": {"name": "Pro Pack", "credits": 200, "price_cents": 1499},
    "mega": {"name": "Mega Pack", "credits": 500, "price_cents": 2999},
}


async def create_checkout_session(user: User, package_id: str) -> str:
    package = CREDIT_PACKAGES.get(package_id)
    if not package:
        raise ValueError(f"Unknown package: {package_id}")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": package["name"]},
                    "unit_amount": package["price_cents"],
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.stripe_success_url,
        cancel_url=settings.stripe_cancel_url,
        metadata={
            "user_id": str(user.id),
            "package_id": package_id,
            "credits": str(package["credits"]),
        },
    )
    return session.url


async def handle_checkout_completed(session: dict):
    metadata = session.get("metadata", {})
    user_id = metadata.get("user_id")
    package_id = metadata.get("package_id")
    credits = int(metadata.get("credits", 0))

    user = await User.get(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    package = CREDIT_PACKAGES.get(package_id, {})

    await add_credits(user, credits)

    await Payment(
        user_id=user_id,
        stripe_session_id=session["id"],
        amount_cents=session.get("amount_total", 0),
        credits_added=credits,
        package_name=package.get("name", package_id),
    ).insert()
