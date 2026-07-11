# Voice Task Bot

Телеграм-бот «голос → задача». Принимает голосовое сообщение и превращает его
в текст через Whisper на бесплатном тарифе Groq API.

**Текущий статус — MVP:** приём голосовых + транскрипция, без извлечения задачи.

## Дорожная карта

- [x] Скелет бота на aiogram 3, приём voice message
- [x] Транскрипция через Whisper (Groq API, бесплатно)
- [ ] Извлечение структурированной задачи (title, deadline, priority,
      description) через Llama на Groq
- [ ] Карточка задачи с inline-кнопками «Сохранить» / «Исправить»
- [ ] Сохранение подтверждённых задач в SQLite

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# заполни TELEGRAM_BOT_TOKEN и GROQ_API_KEY

python main.py
```

## Структура

```
├── main.py           # точка входа, запуск polling
├── config.py         # переменные окружения (.env через python-dotenv)
├── handlers.py       # /start, голосовые сообщения, fallback
└── transcription.py  # обёртка над Whisper (Groq API)
```
