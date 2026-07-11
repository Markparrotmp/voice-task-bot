#!/usr/bin/env bash
# Автоустановка бота «голос → задача» на сервер Ubuntu/Debian.
# Запуск от root одной командой:
#   bash <(curl -fsSL https://raw.githubusercontent.com/Markparrotmp/voice-task-bot/main/setup.sh)
# Скрипт можно запускать повторно — он просто обновит бота и перезапустит его.

set -euo pipefail

REPO_URL="https://github.com/Markparrotmp/voice-task-bot.git"
APP_DIR="/opt/voicetaskbot"

if [ "$(id -u)" -ne 0 ]; then
    echo "Запусти скрипт от root (на VPS ты и так root)." >&2
    exit 1
fi

echo "=== 1/5 Установка Python и git ==="
apt-get update -y
apt-get install -y python3-venv git

echo "=== 2/5 Загрузка кода бота ==="
if [ -d "$APP_DIR/.git" ]; then
    git -C "$APP_DIR" pull
else
    git clone "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"

echo "=== 3/5 Установка зависимостей ==="
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

echo "=== 4/5 Настройка токенов ==="
if [ -f .env ]; then
    echo "Файл .env уже есть — оставляю как есть."
else
    read -rp "Вставь токен бота от @BotFather: " BOT_TOKEN
    read -rp "Вставь ключ Groq (gsk_...): " GROQ_KEY
    printf 'TELEGRAM_BOT_TOKEN=%s\nGROQ_API_KEY=%s\n' "$BOT_TOKEN" "$GROQ_KEY" > .env
    chmod 600 .env
fi

echo "=== 5/5 Запуск службы ==="
cp voicetaskbot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable voicetaskbot >/dev/null 2>&1
systemctl restart voicetaskbot
sleep 3

if systemctl is-active --quiet voicetaskbot; then
    echo ""
    echo "✅ Готово! Бот запущен и будет стартовать сам после перезагрузок."
    echo "Проверь: отправь боту /start и голосовое сообщение в Telegram."
    echo "Логи бота: journalctl -u voicetaskbot -n 30"
else
    echo ""
    echo "❌ Бот не запустился. Посмотри логи:"
    journalctl -u voicetaskbot -n 20 --no-pager || true
    exit 1
fi
