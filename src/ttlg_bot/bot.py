"""Сборка Bot, Dispatcher и роутеров."""

from __future__ import annotations

from aiogram import Bot, Dispatcher

from ttlg_bot.handlers.chat import create_chat_router
from ttlg_bot.services.chat_service import ChatService


def create_bot(token: str) -> Bot:
    # Без parse_mode: ответы LLM могут содержать произвольный текст
    return Bot(token=token)


def create_dispatcher(chat_service: ChatService) -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(create_chat_router(chat_service))
    return dp
