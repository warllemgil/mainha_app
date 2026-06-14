import httpx

from app.config import Settings, get_settings


class GeminiServiceError(RuntimeError):
    pass


class GeminiService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def generate_response(
        self,
        user_text: str,
        *,
        session_id: str | None = None,
    ) -> str:
        if not self.settings.gemini_api_key:
            raise GeminiServiceError("GEMINI_API_KEY nao configurada no backend.")

        prompt = self._build_prompt(user_text, session_id=session_id)
        url = (
            f"{self.settings.gemini_api_base_url.rstrip('/')}/models/"
            f"{self.settings.gemini_model}:generateContent"
        )
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.6,
                "topP": 0.9,
                "maxOutputTokens": 800,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
                response = await client.post(
                    url,
                    params={"key": self.settings.gemini_api_key},
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise GeminiServiceError(f"Falha de rede ao chamar Gemini: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text[:500]
            raise GeminiServiceError(f"Gemini retornou HTTP {response.status_code}: {detail}")

        data = response.json()
        text = self._extract_text(data)
        if not text:
            raise GeminiServiceError("Gemini nao retornou texto utilizavel.")
        return text.strip()

    def _build_prompt(self, user_text: str, *, session_id: str | None = None) -> str:
        context = (
            "Voce e Mainha, um assistente conversacional leve em portugues do Brasil. "
            "Responda de forma direta, natural e adequada para ser falada em voz alta. "
            "Quando precisar de uma acao externa ainda nao disponivel, explique a limitacao "
            "em uma frase curta."
        )
        session = f"\nSessao: {session_id}" if session_id else ""
        return f"{context}{session}\n\nUsuario: {user_text}"

    def _extract_text(self, data: dict) -> str:
        candidates = data.get("candidates") or []
        parts: list[str] = []
        for candidate in candidates:
            content = candidate.get("content") or {}
            for part in content.get("parts") or []:
                text = part.get("text")
                if text:
                    parts.append(text)
        return "\n".join(parts)
