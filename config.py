"""Загрузка настроек из переменных окружения (.env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def validate() -> None:
    """Падает с понятной ошибкой, если не хватает обязательных переменных."""
    missing = [
        name
        for name, value in {
            "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
            "OPENAI_API_KEY": OPENAI_API_KEY,
        }.items()
        if not value
    ]
    if missing:
        raise SystemExit(
            "Не заданы переменные окружения: "
            + ", ".join(missing)
            + ". Скопируй .env.example в .env и заполни значения."
        )
