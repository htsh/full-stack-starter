from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser


class User(BeanieBaseUser, Document):
    credits: int = 0
    stripe_customer_id: str | None = None

    class Settings(BeanieBaseUser.Settings):
        name = "users"
