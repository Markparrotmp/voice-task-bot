"""Транскрипция аудио через Groq API (Whisper, бесплатный тариф)."""

import io

from groq import AsyncGroq

import config

# Быстрая мультиязычная модель Whisper, доступна на бесплатном тарифе Groq.
WHISPER_MODEL = "whisper-large-v3-turbo"

_client: AsyncGroq | None = None


def _get_client() -> AsyncGroq:
    global _client
    if _client is None:
        _client = AsyncGroq(api_key=config.GROQ_API_KEY)
    return _client


async def transcribe(audio: bytes, filename: str = "voice.ogg") -> str:
    """Принимает байты аудиофайла, возвращает расшифрованный текст.

    Telegram присылает голосовые в формате OGG/Opus — Whisper понимает
    его напрямую, перекодировка не нужна. Имя файла обязательно: по его
    расширению API определяет формат.
    """
    buffer = io.BytesIO(audio)
    buffer.name = filename
    result = await _get_client().audio.transcriptions.create(
        model=WHISPER_MODEL,
        file=buffer,
    )
    return result.text.strip()
