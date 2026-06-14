import base64

import httpx

from app.config import Settings, get_settings


class SuperVozServiceError(RuntimeError):
    pass


class SuperVozAudioResult:
    def __init__(
        self,
        *,
        audio_base64: str | None = None,
        audio_url: str | None = None,
        content_type: str | None = None,
    ) -> None:
        self.audio_base64 = audio_base64
        self.audio_url = audio_url
        self.content_type = content_type


class SuperVozService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def synthesize(
        self,
        text: str,
        *,
        voice: str | None = None,
        mode: str | None = None,
        nfe_step: int | None = None,
        return_audio_base64: bool = True,
    ) -> SuperVozAudioResult:
        if not self.settings.supervoz_api_url:
            raise SuperVozServiceError("SUPERVOZ_API_URL nao configurada.")

        headers = {"Content-Type": "application/json"}
        if self.settings.supervoz_api_token:
            headers["Authorization"] = f"Bearer {self.settings.supervoz_api_token}"

        payload = {
            "voice": voice or self.settings.supervoz_voice,
            "text": text,
            "speed": self.settings.supervoz_speed,
            "mode": mode or self.settings.supervoz_mode,
            "nfe_step": nfe_step or self.settings.supervoz_nfe_step,
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
                response = await client.post(
                    f"{self.settings.normalized_supervoz_api_url}/tts",
                    headers=headers,
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise SuperVozServiceError(f"Falha de rede ao chamar SuperVoz: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text[:500]
            raise SuperVozServiceError(f"SuperVoz retornou HTTP {response.status_code}: {detail}")

        content_type = response.headers.get("content-type", "audio/wav").split(";")[0]
        if content_type.startswith("audio/") or content_type == "application/octet-stream":
            if not return_audio_base64:
                # O endpoint atual da extensao toca base64 com data URL. URL publica pode ser
                # adicionada depois se o orquestrador passar a armazenar arquivos de resposta.
                return SuperVozAudioResult(content_type=content_type)
            return SuperVozAudioResult(
                audio_base64=base64.b64encode(response.content).decode("ascii"),
                content_type=content_type,
            )

        data = response.json()
        return SuperVozAudioResult(
            audio_base64=data.get("audio_base64"),
            audio_url=data.get("audio_url") or data.get("audio_path"),
            content_type=data.get("audio_content_type") or data.get("content_type") or "audio/wav",
        )
