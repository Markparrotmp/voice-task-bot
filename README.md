# Voice Task Bot

Телеграм-бот «голос → задача». Принимает голосовое сообщение и превращает его
в текст через OpenAI Whisper API.

**Текущий статус — MVP:** приём голосовых + транскрипция, без извлечения задачи.

## Дорожная карта

- [x] Скелет бота на aiogram 3, приём voice message
- [x] Транскрипция через Whisper API
- [ ] Извлечение структурированной задачи (title, deadline, priority,
      description) через Anthropic Claude API
- [ ] Карточка задачи с inline-кнопками «Сохранить» / «Исправить»
- [ ] Сохранение подтверждённых задач в SQLite

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# заполни TELEGRAM_BOT_TOKEN и OPENAI_API_KEY

python main.py
```

## Структура

```
├── main.py           # точка входа, запуск polling
├── config.py         # переменные окружения (.env через python-dotenv)
├── handlers.py       # /start, голосовые сообщения, fallback
└── transcription.py  # обёртка над Whisper API
```
