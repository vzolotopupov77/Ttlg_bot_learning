# Ttlg_bot_learning

Telegram-бот с LLM (OpenRouter) для поддержки учёбы по математике — MVP: диалог в памяти, без БД.

## Требования

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) для зависимостей

## Установка

```bash
make install
```

Или: `uv sync`

## Настройка

1. Скопируйте `.env.example` в `.env`.
2. Укажите `TELEGRAM_BOT_TOKEN` (от [@BotFather](https://t.me/BotFather)) и `OPENROUTER_API_KEY` ([OpenRouter](https://openrouter.ai/keys)).
3. При необходимости измените `LLM_MODEL`, `OPENROUTER_BASE_URL`, `LOG_LEVEL`, `HISTORY_DEPTH`.

Файл **`.env` должен лежать в корне репозитория** (рядом с `pyproject.toml`). Значения можно без кавычек: `TELEGRAM_BOT_TOKEN=123456:ABC...`

**Приоритет:** переменные окружения процесса (в т.ч. заданные в Windows «Переменные среды» или в текущей сессии PowerShell) **перекрывают** строки из `.env`. Если после правки `.env` всё ещё виден старый токен — проверьте `echo $env:TELEGRAM_BOT_TOKEN` в PowerShell и при необходимости удалите переменную или откройте новый терминал.

Если в PowerShell токен **пустой** — это нормально: тогда значение должно быть **только в `.env`**. При старте в лог пишется путь к ожидаемому `.env` и есть ли файл на диске.

Сохраняйте `.env` как **UTF-8**; приложение читает файл с поддержкой BOM (типичный случай после «Блокнота» в Windows).

## Запуск

```bash
make run
```

Или: `uv run python -m ttlg_bot`

Бот работает в режиме **long polling**.

## Документация

- [docs/vision.md](docs/vision.md) — техническое видение
- [docs/idea.md](docs/idea.md) — продуктовая идея
