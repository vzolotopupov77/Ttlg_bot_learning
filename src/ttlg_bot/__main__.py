"""Точка входа: логирование и long polling."""

from __future__ import annotations

import asyncio
import logging
import os
import sys

from pydantic import ValidationError

from ttlg_bot.bot import create_bot, create_dispatcher
from ttlg_bot.config import ENV_FILE_PATH, Settings
from ttlg_bot.services.backend_client import BackendClient
from ttlg_bot.services.chat_service import ChatService


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

    tid, _, tsec = settings.telegram_bot_token.partition(":")
    log.info(
        "TELEGRAM_BOT_TOKEN: загружен (bot_id=%s, символов после ':': %d)",
        tid,
        len(tsec),
    )
    base = str(settings.backend_url).rstrip("/")
    log.info("BACKEND_URL: %s (timeout=%.1fs)", base, settings.backend_timeout)

    backend_client = BackendClient(
        base_url=base,
        timeout=settings.backend_timeout,
    )
    chat_service = ChatService(backend_client)

    bot = create_bot(settings.telegram_bot_token)
    dp = create_dispatcher(chat_service)

    logging.getLogger(__name__).info("Starting bot (long polling)")
    try:
        await dp.start_polling(bot)
    finally:
        await backend_client.aclose()


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
