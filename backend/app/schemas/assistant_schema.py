from pydantic import BaseModel, Field


class AssistantChatRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto do usuario ja transcrito.")
    session_id: str | None = Field(default=None, description="Identificador opcional da conversa.")
    return_audio_base64: bool = Field(default=True)
    voice: str | None = Field(default=None)
    mode: str | None = Field(default=None, pattern="^(fast|balanced|quality)$")
    nfe_step: int | None = Field(default=None, ge=4, le=64)


class AssistantChatResponse(BaseModel):
    user_text: str
    answer_text: str
    audio_base64: str | None = None
    audio_url: str | None = None
    audio_content_type: str | None = None
    provider: str = "gemini"


class AssistantVoiceResponse(AssistantChatResponse):
    transcribed_text: str
    stt_provider: str


class ToolRequest(BaseModel):
    tool_name: str = Field(..., min_length=1)
    input: dict = Field(default_factory=dict)
    dry_run: bool = True


class ToolResponse(BaseModel):
    status: str
    message: str
    result: dict = Field(default_factory=dict)
