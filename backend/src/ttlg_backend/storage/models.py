"""SQLAlchemy ORM models (async). Aligned with docs/data-model.md."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class UserRole(StrEnum):
    student = "student"
    teacher = "teacher"


class LessonStatus(StrEnum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class AssignmentStatus(StrEnum):
    pending = "pending"
    submitted = "submitted"
    overdue = "overdue"


class DialogueChannel(StrEnum):
    telegram = "telegram"
    web = "web"


class MessageRole(StrEnum):
    user = "user"
    assistant = "assistant"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_telegram_id", "telegram_id", unique=True),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", native_enum=True, values_callable=lambda e: [i.value for i in e]),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
    class_label: Mapped[str | None] = mapped_column(String(32), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    lessons_as_student: Mapped[list[Lesson]] = relationship(
        back_populates="student",
        foreign_keys="Lesson.student_id",
    )
    lessons_as_teacher: Mapped[list[Lesson]] = relationship(
        back_populates="teacher",
        foreign_keys="Lesson.teacher_id",
    )
    assignments: Mapped[list[Assignment]] = relationship(back_populates="student")
    progress_rows: Mapped[list[Progress]] = relationship(back_populates="student")
    dialogues: Mapped[list[Dialogue]] = relationship(back_populates="student")


class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (
        Index("ix_lessons_scheduled_at", "scheduled_at"),
        CheckConstraint("duration_minutes > 0", name="ck_lessons_duration_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(512), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(
        SmallInteger(),
        nullable=False,
        default=60,
        server_default="60",
    )
    status: Mapped[LessonStatus] = mapped_column(
        SQLEnum(LessonStatus, name="lesson_status", native_enum=True, values_callable=lambda e: [i.value for i in e]),
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    student: Mapped[User] = relationship(
        back_populates="lessons_as_student",
        foreign_keys=[student_id],
    )
    teacher: Mapped[User] = relationship(
        back_populates="lessons_as_teacher",
        foreign_keys=[teacher_id],
    )
    assignments: Mapped[list[Assignment]] = relationship(back_populates="lesson")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[AssignmentStatus] = mapped_column(
        SQLEnum(
            AssignmentStatus,
            name="assignment_status",
            native_enum=True,
            values_callable=lambda e: [i.value for i in e],
        ),
    )

    lesson: Mapped[Lesson | None] = relationship(back_populates="assignments")
    student: Mapped[User] = relationship(back_populates="assignments")


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("student_id", "period_start", "period_end", name="uq_progress_student_period"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    lessons_completed: Mapped[int] = mapped_column(nullable=False, default=0)
    assignments_done: Mapped[int] = mapped_column(nullable=False, default=0)
    assignments_total: Mapped[int] = mapped_column(nullable=False, default=0)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    student: Mapped[User] = relationship(back_populates="progress_rows")


class Dialogue(Base):
    __tablename__ = "dialogues"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[DialogueChannel] = mapped_column(
        SQLEnum(
            DialogueChannel,
            name="dialogue_channel",
            native_enum=True,
            values_callable=lambda e: [i.value for i in e],
        ),
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    student: Mapped[User] = relationship(back_populates="dialogues")
    messages: Mapped[list[Message]] = relationship(
        back_populates="dialogue",
        order_by="Message.created_at",
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (Index("ix_messages_dialogue_created", "dialogue_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dialogue_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("dialogues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[MessageRole] = mapped_column(
        SQLEnum(MessageRole, name="message_role", native_enum=True, values_callable=lambda e: [i.value for i in e]),
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    dialogue: Mapped[Dialogue] = relationship(back_populates="messages")
