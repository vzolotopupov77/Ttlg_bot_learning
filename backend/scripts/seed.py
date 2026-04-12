"""Dev seed: teacher + student + lesson + assignment (idempotent).

Запуск: make backend-db-seed
        uv run --package ttlg-backend python backend/scripts/seed.py

Перед запуском: `make backend-db-up` и `make backend-db-migrate` (схема должна существовать).

Учётные данные преподавателя для POST /v1/auth/login — из .env через pydantic-settings
(TEACHER_NAME, TEACHER_EMAIL, TEACHER_DEFAULT_PASSWORD). Не используйте os.environ вручную:
значения из файла .env подхватываются только при чтении Settings.

DEV_STUDENT_TELEGRAM_ID = 111111111 — фиксированный id тестового ученика.
Используйте это значение при ручном тестировании POST /v1/dialogue/message.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ttlg_backend.config import Settings, get_settings
from ttlg_backend.services.auth_service import hash_password
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


async def _find_existing_teacher(session: AsyncSession, settings: Settings) -> User | None:
    """Один dev-учитель: ищем по email, затем по имени из .env, затем legacy «Преподаватель», иначе любой teacher."""
    email_norm = settings.teacher_email.strip().lower()
    if email_norm:
        q = select(User).where(User.role == UserRole.teacher, func.lower(User.email) == email_norm)
        row = await session.execute(q)
        found = row.scalar_one_or_none()
        if found is not None:
            return found
    name = settings.teacher_name.strip()
    if name:
        q = select(User).where(User.role == UserRole.teacher, User.name == name)
        row = await session.execute(q)
        found = row.scalar_one_or_none()
        if found is not None:
            return found
    q = select(User).where(User.role == UserRole.teacher, User.name == "Преподаватель")
    row = await session.execute(q)
    found = row.scalar_one_or_none()
    if found is not None:
        return found
    q = select(User).where(User.role == UserRole.teacher).limit(1)
    row = await session.execute(q)
    return row.scalar_one_or_none()


async def _get_or_create_teacher(session: AsyncSession, settings: Settings) -> User:
    teacher = await _find_existing_teacher(session, settings)
    if teacher is None:
        teacher = User(
            role=UserRole.teacher,
            name=settings.teacher_name.strip(),
            email=settings.teacher_email.strip() or None,
        )
        session.add(teacher)
        await session.flush()
        log.info("Создан преподаватель: %s (%s)", teacher.id, teacher.name)
    else:
        log.info("Обновляем существующего преподавателя: %s", teacher.id)
    teacher.name = settings.teacher_name.strip()
    teacher.email = settings.teacher_email.strip() or None
    await _apply_teacher_login_credentials(session, teacher, settings)
    return teacher


async def _apply_teacher_login_credentials(session: AsyncSession, teacher: User, settings: Settings) -> None:
    """email + bcrypt-хеш для POST /v1/auth/login (роль teacher)."""
    pwd_secret = settings.teacher_default_password
    password = pwd_secret.get_secret_value().strip() if pwd_secret is not None else ""
    if password:
        teacher.password_hash = hash_password(password)
        log.info(
            "У преподавателя заданы имя=%r email=%r и пароль из TEACHER_DEFAULT_PASSWORD",
            teacher.name,
            teacher.email,
        )
    else:
        log.warning(
            "TEACHER_DEFAULT_PASSWORD пуст — вход POST /v1/auth/login для преподавателя недоступен. "
            "Задайте в .env и перезапустите сид.",
        )
    await session.flush()


async def _get_or_create_student(session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.telegram_id == DEV_STUDENT_TELEGRAM_ID))
    student = result.scalar_one_or_none()
    if student is None:
        student = User(
            role=UserRole.student,
            name="Ученик",
            telegram_id=DEV_STUDENT_TELEGRAM_ID,
            class_label="10А",
        )
        session.add(student)
        await session.flush()
        log.info("Создан ученик: %s (telegram_id=%d)", student.id, DEV_STUDENT_TELEGRAM_ID)
    else:
        log.info("Ученик уже существует: %s", student.id)
    return student


async def _get_or_create_lesson(session: AsyncSession, student: User, teacher: User) -> Lesson:
    result = await session.execute(
        select(Lesson).where(Lesson.student_id == student.id, Lesson.topic == "Seed-занятие")
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


async def _get_or_create_assignment(session: AsyncSession, student: User, lesson: Lesson) -> Assignment:
    result = await session.execute(
        select(Assignment).where(Assignment.lesson_id == lesson.id, Assignment.student_id == student.id)
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


async def seed(session: AsyncSession, settings: Settings) -> None:
    teacher = await _get_or_create_teacher(session, settings)
    student = await _get_or_create_student(session)
    lesson = await _get_or_create_lesson(session, student, teacher)
    await _get_or_create_assignment(session, student, lesson)
    await session.commit()


async def main() -> None:
    get_settings.cache_clear()
    settings = get_settings()
    if not settings.database_url:
        msg = "DATABASE_URL не задан — проверьте .env"
        raise RuntimeError(msg)

    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with session_factory() as session:
            await seed(session, settings)
    finally:
        await engine.dispose()

    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
