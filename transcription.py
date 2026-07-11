"""Транскрипция аудио локальной моделью Whisper (faster-whisper).

Модель крутится прямо на сервере: без внешних API, лимитов и
региональных блокировок. Первый запуск скачивает модель с Hugging Face
(~150–500 МБ в зависимости от размера).
"""

import asyncio
import io

from faster_whisper import WhisperModel

import config

_model: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel(
            config.WHISPER_MODEL,
            device="cpu",
            compute_type="int8",
        )
    return _model


def preload() -> None:
    """Скачивает и загружает модель заранее, чтобы первое голосовое
    не ждало несколько минут."""
    _get_model()


def _transcribe_sync(audio: bytes) -> str:
    segments, _info = _get_model().transcribe(
        io.BytesIO(audio),
        vad_filter=True,  # отсекает тишину в начале/конце
    )
    return " ".join(segment.text.strip() for segment in segments).strip()


async def transcribe(audio: bytes, filename: str = "voice.ogg") -> str:
    """Принимает байты аудиофайла (OGG/Opus от Telegram — напрямую),
    возвращает расшифрованный текст.

    Распознавание — блокирующая CPU-работа, поэтому уводим его в поток,
    чтобы бот продолжал отвечать на другие сообщения.
    """
    return await asyncio.to_thread(_transcribe_sync, audio)
