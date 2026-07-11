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

## Установка на сервер (рекомендуемый способ)

Понадобятся два токена (оба бесплатные):

- **Токен бота** — в Telegram у [@BotFather](https://t.me/BotFather): `/newbot`,
  придумать имя и юзернейм, скопировать токен вида `1234567890:AAE…`
- **Ключ Groq** — на [console.groq.com](https://console.groq.com):
  API Keys → Create API Key, скопировать ключ вида `gsk_…`

Дальше на сервере одна команда от root:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Markparrotmp/voice-task-bot/main/setup.sh)
```

Скрипт сам ставит зависимости, спрашивает оба токена и запускает бота как
systemd-службу `voicetaskbot` (переживает перезагрузки). Повторный запуск
скрипта обновляет бота до свежей версии.

Полезные команды на сервере:

```bash
systemctl status voicetaskbot        # работает ли бот
journalctl -u voicetaskbot -n 30     # последние логи
systemctl restart voicetaskbot       # перезапуск
```

## Запуск локально (для разработки)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# заполни TELEGRAM_BOT_TOKEN и GROQ_API_KEY

python main.py
```

## Структура

```
├── main.py               # точка входа, запуск polling
├── config.py             # переменные окружения (.env через python-dotenv)
├── handlers.py           # /start, голосовые сообщения, fallback
├── transcription.py      # обёртка над Whisper (Groq API)
├── setup.sh              # однокомандная установка на сервер
└── voicetaskbot.service  # systemd-служба для автозапуска
```
