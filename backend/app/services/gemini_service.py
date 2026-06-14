import logging

from google import genai
from google.genai import types

from app.config import Settings, get_settings


class GeminiServiceError(RuntimeError):
    pass


LOGGER = logging.getLogger("mainha.gemini")


class GeminiService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key)

    async def generate_response(
        self,
        user_text: str,
        *,
        session_id: str | None = None,
    ) -> str:
        if not self.settings.gemini_api_key:
            raise GeminiServiceError("GEMINI_API_KEY nao configurada no backend.")

        prompt = self._build_prompt(user_text, session_id=session_id)
        model = self.settings.gemini_model
        LOGGER.info(
            "Chamando Gemini modelo=%s session_id=%s prompt_chars=%s",
            model,
            session_id or "-",
            len(prompt),
        )
        try:
            response = await self._generate_content(
                model=model,
                prompt=prompt,
            )
        except Exception as exc:
            raise GeminiServiceError(f"Falha ao chamar Gemini: {exc}") from exc

        text = self._extract_text(response)
        if not text:
            raise GeminiServiceError("Gemini nao retornou texto utilizavel.")
        return text.strip()

    async def _generate_content(self, *, model: str, prompt: str):
        import asyncio

        config = types.GenerateContentConfig(
            temperature=0.6,
            top_p=0.9,
            max_output_tokens=800,
        )
        return await asyncio.to_thread(
            self.client.models.generate_content,
            model=model,
            contents=[prompt],
            config=config,
        )

    def _extract_text(self, response) -> str:
        text = getattr(response, "text", "") or ""
        if text:
            return text

        candidates = getattr(response, "candidates", None) or []
        parts: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            for part in getattr(content, "parts", None) or []:
                part_text = getattr(part, "text", None)
                if part_text:
                    parts.append(part_text)
        return "\n".join(parts)

    def _build_prompt(self, user_text: str, *, session_id: str | None = None) -> str:
        context = (
            "Voce e Mainha, um assistente conversacional leve em portugues do Brasil. "
            "Responda de forma direta, natural e adequada para ser falada em voz alta. "
            "Quando precisar de uma acao externa ainda nao disponivel, explique a limitacao "
            "em uma frase curta."
        )
        session = f"\nSessao: {session_id}" if session_id else ""
        return f"{context}{session}\n\nUsuario: {user_text}"
