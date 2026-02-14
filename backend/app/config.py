from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "fullstack_ai_app"

    # Auth / JWT
    jwt_secret: str = "change-me"
    reset_password_secret: str = "change-me"
    verification_secret: str = "change-me"

    # OAuth
    google_oauth_client_id: str = ""
    google_oauth_client_secret: str = ""
    github_oauth_client_id: str = ""
    github_oauth_client_secret: str = ""

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_success_url: str = "http://localhost:5173/dashboard?payment=success"
    stripe_cancel_url: str = "http://localhost:5173/pricing?payment=cancelled"

    # App
    backend_cors_origins: str = "http://localhost:5173"
    initial_free_credits: int = 10


settings = Settings()
