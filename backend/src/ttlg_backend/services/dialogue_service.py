"""Orchestration for POST /v1/dialogue/message."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.llm.client import LLMClient
from ttlg_backend.llm.errors import LLMUnavailableError
from ttlg_backend.llm.prompt import (
    StudentContextForPrompt,
    build_system_prompt,
    format_assignment_line,
    format_lesson_line,
)
from ttlg_backend.storage.models import DialogueChannel, MessageRole
from ttlg_backend.storage.repositories import assignments as assignments_repo
from ttlg_backend.storage.repositories import dialogues as dialogues_repo
from ttlg_backend.storage.repositories import lessons as lessons_repo
from ttlg_backend.storage.repositories import users as users_repo


@dataclass
class DialogueSuccess:
    dialogue_id: UUID
    assistant_message_id: UUID
    text: str
    created_at: datetime


class DialogueNotFound(Exception):
    """Unknown dialogue or not owned by student."""


class UserNotFound(Exception):
    """No student with this telegram_id."""


async def _build_student_context(session: AsyncSession, student_id: UUID, student_name: str) -> StudentContextForPrompt:
    lessons = await lessons_repo.list_recent_lessons_for_student(session, student_id, limit=8)
    assigns = await assignments_repo.list_recent_assignments_for_student(session, student_id, limit=8)
    lesson_lines = [format_lesson_line(l.topic, l.scheduled_at, l.status.value) for l in lessons]
    assign_lines = [
        format_assignment_line(a.description, a.due_date, a.status.value) for a in assigns
    ]
    return StudentContextForPrompt(
        student_name=student_name,
        upcoming_lessons=lesson_lines,
        recent_assignments=assign_lines,
    )


async def process_dialogue_message(
    session: AsyncSession,
    llm: LLMClient,
    *,
    telegram_id: int,
    text: str,
    dialogue_id: UUID | None,
    channel: DialogueChannel = DialogueChannel.telegram,
) -> DialogueSuccess:
    user = await users_repo.get_student_by_telegram_id(session, telegram_id)
    if user is None:
        raise UserNotFound

    if dialogue_id is not None:
        dialogue = await dialogues_repo.get_dialogue_owned_by_student(
            session,
            dialogue_id,
            user.id,
        )
        if dialogue is None:
            raise DialogueNotFound
    else:
        dialogue = await dialogues_repo.create_dialogue(
            session,
            student_id=user.id,
            channel=channel,
        )

    try:
        await dialogues_repo.add_message(
            session,
            dialogue_id=dialogue.id,
            role=MessageRole.user,
            content=text,
        )

        ctx = await _build_student_context(session, user.id, user.name)
        system_prompt = build_system_prompt(ctx)

        reply_text = await llm.complete_chat(system_prompt=system_prompt, user_message=text)

        assistant_msg = await dialogues_repo.add_message(
            session,
            dialogue_id=dialogue.id,
            role=MessageRole.assistant,
            content=reply_text,
        )
        await session.commit()
        await session.refresh(assistant_msg)
    except LLMUnavailableError:
        await session.rollback()
        raise
    except Exception:
        await session.rollback()
        raise
    created_at = assistant_msg.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    else:
        created_at = created_at.astimezone(UTC)
    return DialogueSuccess(
        dialogue_id=dialogue.id,
        assistant_message_id=assistant_msg.id,
        text=reply_text,
        created_at=created_at,
    )
