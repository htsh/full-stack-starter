from app.models.user import User


async def add_credits(user: User, amount: int) -> User:
    user.credits += amount
    await user.save()
    return user


async def deduct_credits(user: User, amount: int) -> User:
    if user.credits < amount:
        raise ValueError(f"Insufficient credits: have {user.credits}, need {amount}")
    user.credits -= amount
    await user.save()
    return user
