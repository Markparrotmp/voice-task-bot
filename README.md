# Voice Task Bot

Телеграм-бот «голос → задача». Принимает голосовое сообщение и превращает его
в текст локальной моделью Whisper (faster-whisper) — без внешних AI-API,
лимитов и региональных блокировок, полностью бесплатно.

**Текущий статус — MVP:** приём голосовых + транскрипция, без извлечения задачи.

## Дорожная карта

- [x] Скелет бота на aiogram 3, приём voice message
- [x] Транскрипция локальным Whisper (faster-whisper, без внешних API)
- [ ] Извлечение структурированной задачи (title, deadline, priority,
      description)
- [ ] Карточка задачи с inline-кнопками «Сохранить» / «Исправить»
- [ ] Сохранение подтверждённых задач в SQLite

## Установка на сервер (рекомендуемый способ)

Понадобится только **токен бота** — в Telegram у
[@BotFather](https://t.me/BotFather): `/newbot`, придумать имя и юзернейм,
скопировать токен вида `1234567890:AAE…`

Дальше на сервере одна команда от root:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Markparrotmp/voice-task-bot/main/setup.sh)
```

Скрипт сам ставит зависимости, спрашивает токен и запускает бота как
systemd-службу `voicetaskbot` (переживает перезагрузки). Повторный запуск
скрипта обновляет бота до свежей версии. При первом старте бот скачивает
модель распознавания (~150 МБ) — подожди пару минут, прогресс виден в логах.

Размер модели настраивается переменной `WHISPER_MODEL` в
`/opt/voicetaskbot/.env` (см. `.env.example`): `base` по умолчанию,
`small` — качественнее, если на сервере от 2 ГБ оперативки.

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
# заполни TELEGRAM_BOT_TOKEN

python main.py
```

## Структура

```
├── main.py               # точка входа, запуск polling
├── config.py             # переменные окружения (.env через python-dotenv)
├── handlers.py           # /start, голосовые сообщения, fallback
├── transcription.py      # локальный Whisper (faster-whisper)
├── setup.sh              # однокомандная установка на сервер
└── voicetaskbot.service  # systemd-служба для автозапуска
```
