from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager
from fastapi_users_db_beanie import BeanieUserDatabase, ObjectIDIDMixin

from app.config import settings
from app.models.user import User


async def get_user_db():
    yield BeanieUserDatabase(User)


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.reset_password_secret
    verification_token_secret = settings.verification_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        user.credits = settings.initial_free_credits
        await user.save()
        print(f"User {user.id} registered, granted {settings.initial_free_credits} free credits.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} forgot password. Reset token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
