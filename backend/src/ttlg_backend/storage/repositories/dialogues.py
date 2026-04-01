"""Dialogue and message persistence helpers."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import Dialogue, DialogueChannel, Message, MessageRole


async def get_dialogue_owned_by_student(
    session: AsyncSession,
    dialogue_id: UUID,
    student_id: UUID,
) -> Dialogue | None:
    stmt = select(Dialogue).where(Dialogue.id == dialogue_id, Dialogue.student_id == student_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_dialogue(
    session: AsyncSession,
    *,
    student_id: UUID,
    channel: DialogueChannel = DialogueChannel.telegram,
) -> Dialogue:
    dialogue = Dialogue(student_id=student_id, channel=channel)
    session.add(dialogue)
    await session.flush()
    return dialogue


async def add_message(
    session: AsyncSession,
    *,
    dialogue_id: UUID,
    role: MessageRole,
    content: str,
) -> Message:
    message = Message(dialogue_id=dialogue_id, role=role, content=content)
    session.add(message)
    await session.flush()
    return message


async def list_messages_for_dialogue(
    session: AsyncSession,
    dialogue_id: UUID,
    *,
    limit: int = 50,
) -> list[Message]:
    stmt = select(Message).where(Message.dialogue_id == dialogue_id).order_by(Message.created_at.asc()).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())
