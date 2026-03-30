"""System prompt + student context for the assistant."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class StudentContextForPrompt:
    """Serializable context from DB for LLM."""

    student_name: str
    upcoming_lessons: list[str]
    recent_assignments: list[str]


def build_system_prompt(ctx: StudentContextForPrompt | None) -> str:
    base = (
        "You are a helpful learning assistant for a student. "
        "Give clear, concise explanations and encourage understanding. "
        "If you lack schedule or homework details, say so briefly and still help with the question."
    )
    if ctx is None:
        return base

    lines: list[str] = [base, "", f"Student name: {ctx.student_name}.", ""]

    if ctx.upcoming_lessons:
        lines.append("Upcoming / recent lessons:")
        for les in ctx.upcoming_lessons:
            lines.append(f"- {les}")
        lines.append("")
    else:
        lines.append("(No lesson data in the system for this student.)")
        lines.append("")

    if ctx.recent_assignments:
        lines.append("Homework assignments:")
        for a in ctx.recent_assignments:
            lines.append(f"- {a}")
        lines.append("")
    else:
        lines.append("(No homework data in the system for this student.)")
        lines.append("")

    return "\n".join(lines).strip()


def format_lesson_line(topic: str, scheduled_at: datetime, status: str) -> str:
    return f"{scheduled_at.isoformat()} — {topic} ({status})"


def format_assignment_line(description: str, due_date: date, status: str) -> str:
    return f"due {due_date.isoformat()} — {status}: {description[:200]}"
