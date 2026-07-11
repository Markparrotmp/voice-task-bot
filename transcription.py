"""Транскрипция аудио через OpenAI Whisper API."""

import io

from openai import AsyncOpenAI

import config

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
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
        model="whisper-1",
        file=buffer,
    )
    return result.text.strip()
