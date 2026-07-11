"""Обработчики сообщений."""

import io
import logging

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from transcription import transcribe

logger = logging.getLogger(__name__)

router = Router()

# Лимит Telegram на длину текстового сообщения.
MAX_MESSAGE_LENGTH = 4096


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Пришли мне голосовое сообщение — я расшифрую его в текст.\n\n"
        "Скоро научусь превращать голос в структурированную задачу."
    )


@router.message(F.voice)
async def handle_voice(message: Message, bot: Bot) -> None:
    status = await message.answer("🎙 Расшифровываю…")

    try:
        buffer = io.BytesIO()
        await bot.download(message.voice, destination=buffer)
        text = await transcribe(buffer.getvalue())
    except Exception:
        logger.exception("Не удалось расшифровать голосовое сообщение")
        await status.edit_text(
            "😔 Не получилось расшифровать сообщение. Попробуй ещё раз."
        )
        return

    if not text:
        await status.edit_text("🤔 Не расслышал — в сообщении нет речи.")
        return

    reply = f"📝 Расшифровка:\n\n{text}"
    if len(reply) > MAX_MESSAGE_LENGTH:
        reply = reply[: MAX_MESSAGE_LENGTH - 1] + "…"
    await status.edit_text(reply)


@router.message()
async def fallback(message: Message) -> None:
    await message.answer("Пока я понимаю только голосовые сообщения 🎙")
