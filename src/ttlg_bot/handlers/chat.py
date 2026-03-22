"""Входящие сообщения: диалог с LLM."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ttlg_bot.services.chat_service import ChatService

logger = logging.getLogger(__name__)


def create_chat_router(chat_service: ChatService) -> Router:
    router = Router(name="chat")

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        await message.answer(
            "Привет! Я помогу с математикой (7–9 класс, ОГЭ). "
            "Напиши вопрос или задачу текстом.",
        )

    @router.message(F.text)
    async def on_text(message: Message) -> None:
        if not message.from_user or not message.text:
            return
        user_id = message.from_user.id
        text = message.text.strip()
        if not text:
            return

        try:
            answer = await chat_service.reply(user_id, text)
        except Exception:
            logger.exception("Unexpected error handling message user_id=%s", user_id)
            await message.answer("Произошла ошибка. Попробуйте ещё раз.")
            return

        await message.answer(answer)

    return router
