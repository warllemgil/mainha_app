import os
from dataclasses import dataclass
from functools import lru_cache

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_int(name: str, default: int) -> int:
    raw = _env(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = _env(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = "Mainha Assistant Backend"
    app_version: str = "0.1.0"

    gemini_api_key: str = _env("GEMINI_API_KEY")
    gemini_model: str = _env("GEMINI_MODEL", "gemini-1.5-flash")
    gemini_api_base_url: str = _env(
        "GEMINI_API_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta",
    )

    supervoz_api_url: str = _env(
        "SUPERVOZ_API_URL",
        "https://warllemedicao--supervoz-f5-gpu-fastapi-app.modal.run",
    )
    supervoz_api_token: str = _env("SUPERVOZ_API_TOKEN")
    supervoz_voice: str = _env("SUPERVOZ_VOICE", "warllem")
    supervoz_mode: str = _env("SUPERVOZ_MODE", "balanced")
    supervoz_nfe_step: int = _env_int("SUPERVOZ_NFE_STEP", 32)
    supervoz_speed: float = _env_float("SUPERVOZ_SPEED", 1.0)

    assistant_auth_token: str = _env("ASSISTANT_AUTH_TOKEN")
    cors_allow_origins: str = _env("CORS_ALLOW_ORIGINS", "*")
    stt_provider: str = _env("STT_PROVIDER", "frontend")

    request_timeout_seconds: float = _env_float("REQUEST_TIMEOUT_SECONDS", 120.0)

    @property
    def normalized_supervoz_api_url(self) -> str:
        return self.supervoz_api_url.rstrip("/").removesuffix("/tts")

    @property
    def cors_origins(self) -> list[str]:
        if self.cors_allow_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
