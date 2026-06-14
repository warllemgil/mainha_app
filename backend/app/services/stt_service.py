from fastapi import UploadFile

from app.config import Settings, get_settings


class STTServiceError(RuntimeError):
    pass


class STTService:
    """Camada substituivel de STT.

    MVP recomendado: usar Web Speech API no frontend e enviar texto para /assistant/chat.
    Futuras opcoes:
    - Whisper local neste backend.
    - API externa de transcricao.
    - Gemini multimodal/audio, se o custo e latencia fizerem sentido.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def transcribe(self, audio: UploadFile | None, *, text_override: str | None = None) -> str:
        if text_override and text_override.strip():
            return text_override.strip()

        if self.settings.stt_provider == "frontend":
            raise STTServiceError(
                "STT_PROVIDER=frontend: transcreva no app/extensao com Web Speech API "
                "e envie o texto para /assistant/chat."
            )

        raise STTServiceError(
            f"STT_PROVIDER={self.settings.stt_provider} ainda nao implementado."
        )
