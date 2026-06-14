from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings
from app.schemas.assistant_schema import (
    AssistantChatRequest,
    AssistantChatResponse,
    AssistantVoiceResponse,
    ToolRequest,
    ToolResponse,
)
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.services.stt_service import STTService, STTServiceError
from app.services.supervoz_service import SuperVozService, SuperVozServiceError
from app.services.tools_service import ToolsService


settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_assistant_token(
    authorization: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    if not settings.assistant_auth_token:
        return
    expected = f"Bearer {settings.assistant_auth_token}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do Mainha Assistant invalido.",
        )


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "gemini_configured": bool(settings.gemini_api_key),
        "supervoz_configured": bool(settings.supervoz_api_url),
        "assistant_auth_enabled": bool(settings.assistant_auth_token),
        "stt_provider": settings.stt_provider,
    }


@app.post(
    "/assistant/chat",
    response_model=AssistantChatResponse,
    dependencies=[Depends(require_assistant_token)],
)
async def assistant_chat(request: AssistantChatRequest) -> AssistantChatResponse:
    try:
        answer_text = await GeminiService().generate_response(
            request.text,
            session_id=request.session_id,
        )
        audio = await SuperVozService().synthesize(
            answer_text,
            voice=request.voice,
            mode=request.mode,
            nfe_step=request.nfe_step,
            return_audio_base64=request.return_audio_base64,
        )
    except GeminiServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except SuperVozServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return AssistantChatResponse(
        user_text=request.text,
        answer_text=answer_text,
        audio_base64=audio.audio_base64,
        audio_url=audio.audio_url,
        audio_content_type=audio.content_type,
    )


@app.post(
    "/assistant/voice",
    response_model=AssistantVoiceResponse,
    dependencies=[Depends(require_assistant_token)],
)
async def assistant_voice(
    audio: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    session_id: str | None = Form(default=None),
) -> AssistantVoiceResponse:
    try:
        transcribed_text = await STTService().transcribe(audio, text_override=text)
        chat_response = await assistant_chat(
            AssistantChatRequest(text=transcribed_text, session_id=session_id)
        )
    except STTServiceError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    return AssistantVoiceResponse(
        **chat_response.model_dump(),
        transcribed_text=transcribed_text,
        stt_provider=get_settings().stt_provider,
    )


@app.post(
    "/assistant/tools",
    response_model=ToolResponse,
    dependencies=[Depends(require_assistant_token)],
)
async def assistant_tools(request: ToolRequest) -> ToolResponse:
    return await ToolsService().execute(request)
