def data_url_from_base64(audio_base64: str, content_type: str = "audio/wav") -> str:
    return f"data:{content_type};base64,{audio_base64}"
