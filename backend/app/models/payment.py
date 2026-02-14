from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Payment(Document):
    user_id: str
    stripe_session_id: str
    amount_cents: int
    credits_added: int
    package_name: str
    status: str = "completed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "payments"
