"""Точка входа: python main.py"""

import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
import transcription
from handlers import router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config.validate()

    logger = logging.getLogger(__name__)
    logger.info(
        "Загружаю модель Whisper «%s» (первый запуск скачивает её, "
        "это может занять несколько минут)…",
        config.WHISPER_MODEL,
    )
    await asyncio.to_thread(transcription.preload)
    logger.info("Модель загружена")

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Бот запущен, начинаю polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
