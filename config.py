"""Загрузка настроек из переменных окружения (.env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Размер локальной модели Whisper: tiny / base / small / medium.
# Чем больше — тем лучше качество (особенно русского), но тем больше
# оперативки и медленнее расшифровка. base — компромисс для VPS с 1 ГБ RAM,
# small заметно качественнее, если памяти 2 ГБ и больше.
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")


def validate() -> None:
    """Падает с понятной ошибкой, если не хватает обязательных переменных."""
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "Не задана переменная окружения TELEGRAM_BOT_TOKEN. "
            "Скопируй .env.example в .env и заполни значения."
        )
