from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    package_id: str


class CheckoutResponse(BaseModel):
    checkout_url: str
