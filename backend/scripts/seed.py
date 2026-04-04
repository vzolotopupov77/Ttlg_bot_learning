"""Dev seed: teacher + student + lesson + assignment (idempotent).

Запуск: make backend-db-seed
        uv run --package ttlg-backend python backend/scripts/seed.py

DEV_STUDENT_TELEGRAM_ID = 111111111 — фиксированный id тестового ученика.
Используйте это значение при ручном тестировании POST /v1/dialogue/message.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ttlg_backend.config import get_settings
from ttlg_backend.storage.models import (
    Assignment,
    AssignmentStatus,
    Lesson,
    LessonStatus,
    User,
    UserRole,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# Фиксированный telegram_id тестового ученика для dev-окружения.
# Укажите этот id при отправке сообщений через POST /v1/dialogue/message.
DEV_STUDENT_TELEGRAM_ID: int = 111111111


async def _get_or_create_teacher(session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(User.role == UserRole.teacher, User.name == "Преподаватель")
    )
    teacher = result.scalar_one_or_none()
    if teacher is None:
        teacher = User(role=UserRole.teacher, name="Преподаватель")
        session.add(teacher)
        await session.flush()
        log.info("Создан преподаватель: %s", teacher.id)
    else:
        log.info("Преподаватель уже существует: %s", teacher.id)
    return teacher


async def _get_or_create_student(session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(User.telegram_id == DEV_STUDENT_TELEGRAM_ID)
    )
    student = result.scalar_one_or_none()
    if student is None:
        student = User(
            role=UserRole.student,
            name="Ученик",
            telegram_id=DEV_STUDENT_TELEGRAM_ID,
        )
        session.add(student)
        await session.flush()
        log.info("Создан ученик: %s (telegram_id=%d)", student.id, DEV_STUDENT_TELEGRAM_ID)
    else:
        log.info("Ученик уже существует: %s", student.id)
    return student


async def _get_or_create_lesson(
    session: AsyncSession, student: User, teacher: User
) -> Lesson:
    result = await session.execute(
        select(Lesson).where(
            Lesson.student_id == student.id, Lesson.topic == "Seed-занятие"
        )
    )
    lesson = result.scalar_one_or_none()
    if lesson is None:
        lesson = Lesson(
            student_id=student.id,
            teacher_id=teacher.id,
            topic="Seed-занятие",
            scheduled_at=datetime.now(UTC) + timedelta(days=1),
            status=LessonStatus.scheduled,
        )
        session.add(lesson)
        await session.flush()
        log.info("Создано занятие: %s", lesson.id)
    else:
        log.info("Занятие уже существует: %s", lesson.id)
    return lesson


async def _get_or_create_assignment(
    session: AsyncSession, student: User, lesson: Lesson
) -> Assignment:
    result = await session.execute(
        select(Assignment).where(
            Assignment.lesson_id == lesson.id, Assignment.student_id == student.id
        )
    )
    assignment = result.scalar_one_or_none()
    if assignment is None:
        from datetime import date

        assignment = Assignment(
            lesson_id=lesson.id,
            student_id=student.id,
            description="Seed-задание: повторить пройденный материал",
            due_date=date.today() + timedelta(days=7),
            status=AssignmentStatus.pending,
        )
        session.add(assignment)
        await session.flush()
        log.info("Создано задание: %s", assignment.id)
    else:
        log.info("Задание уже существует: %s", assignment.id)
    return assignment


async def seed(session: AsyncSession) -> None:
    teacher = await _get_or_create_teacher(session)
    student = await _get_or_create_student(session)
    lesson = await _get_or_create_lesson(session, student, teacher)
    await _get_or_create_assignment(session, student, lesson)
    await session.commit()


async def main() -> None:
    settings = get_settings()
    if not settings.database_url:
        msg = "DATABASE_URL не задан — проверьте .env"
        raise RuntimeError(msg)

    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with session_factory() as session:
            await seed(session)
    finally:
        await engine.dispose()

    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
