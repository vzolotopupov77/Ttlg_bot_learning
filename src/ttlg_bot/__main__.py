"""Точка входа: логирование и long polling."""

from __future__ import annotations

import asyncio
import logging
import os
import sys

from pydantic import ValidationError

from ttlg_bot.bot import create_bot, create_dispatcher
from ttlg_bot.config import ENV_FILE_PATH, Settings
from ttlg_bot.services.chat_service import ChatService
from ttlg_bot.services.history import HistoryStore
from ttlg_bot.services.llm_client import LLMClient


def _ensure_utf8_stdio() -> None:
    """На Windows консоль часто не UTF-8 — иначе кириллица в логах «ломается»."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _configure_logging(level: str) -> None:
    _ensure_utf8_stdio()
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


async def _main() -> None:
    _configure_logging(os.environ.get("LOG_LEVEL", "INFO"))
    log = logging.getLogger(__name__)
    log.info(
        "Загрузка .env из %s (файл найден: %s)",
        ENV_FILE_PATH,
        ENV_FILE_PATH.exists(),
    )

    settings = Settings()
    logging.getLogger().setLevel(
        getattr(logging, settings.log_level.upper(), logging.INFO),
    )

    # Секреты в лог не пишем — только признак, что значение подхватилось (для отладки)
    tid, _, tsec = settings.telegram_bot_token.partition(":")
    log.info(
        "TELEGRAM_BOT_TOKEN: загружен (bot_id=%s, символов после ':': %d)",
        tid,
        len(tsec),
    )
    log.info(
        "OPENROUTER_API_KEY: загружен (длина ключа: %d символов)",
        len(settings.openrouter_api_key),
    )

    history = HistoryStore(depth=settings.history_depth)
    llm = LLMClient(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        model=settings.llm_model,
    )
    chat_service = ChatService(history, llm)

    bot = create_bot(settings.telegram_bot_token)
    dp = create_dispatcher(chat_service)

    logging.getLogger(__name__).info("Starting bot (long polling)")
    await dp.start_polling(bot)


def main() -> None:
    try:
        asyncio.run(_main())
    except ValidationError as e:
        _ensure_utf8_stdio()
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        log = logging.getLogger(__name__)
        log.error(
            "Ожидаемый файл .env: %s (найден: %s)",
            ENV_FILE_PATH,
            ENV_FILE_PATH.exists(),
        )
        log.error("Ошибка конфигурации:\n%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
