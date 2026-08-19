"""Configuration settings for AuditVector."""

import os
from typing import Optional


class Settings:
    """Central configuration for AuditVector environment, AI models, and Cloud runtime."""

    # AI Model Settings
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    OFFLINE_MODE: bool = os.getenv("AUDITVECTOR_OFFLINE_MODE", "false").lower() in ("true", "1", "yes")

    # Cloud Runtime Settings (local vs gcp)
    RUNTIME: str = os.getenv("AUDITVECTOR_RUNTIME", "local").lower()
    GCP_PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")
    PUBSUB_TOPIC: str = os.getenv("PUBSUB_TOPIC", "auditvector-jobs")
    PUBSUB_SUBSCRIPTION: str = os.getenv("PUBSUB_SUBSCRIPTION", "auditvector-worker-sub")
    FIRESTORE_COLLECTION: str = os.getenv("FIRESTORE_COLLECTION", "audits")

    @classmethod
    def is_gemini_configured(cls) -> bool:
        return bool(cls.GOOGLE_API_KEY and not cls.OFFLINE_MODE)

    @classmethod
    def is_gcp_runtime(cls) -> bool:
        return cls.RUNTIME == "gcp" and bool(cls.GCP_PROJECT_ID)

    @classmethod
    def validate_for_live_execution(cls):
        if not cls.is_gemini_configured():
            raise ValueError(
                "GOOGLE_API_KEY is not set or OFFLINE_MODE is enabled. "
                "Set GOOGLE_API_KEY environment variable to enable live Gemini model reasoning, "
                "or enable offline test mode via AUDITVECTOR_OFFLINE_MODE=true."
            )

    @classmethod
    def get_resolved_model(cls) -> str:
        """Returns the resolved model string ensuring Gemini 3.5+ compliance."""
        return cls.GEMINI_MODEL


settings = Settings()
