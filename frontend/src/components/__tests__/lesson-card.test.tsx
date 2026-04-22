import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"

import { LessonCard } from "@/components/lesson-card"
import type { ScheduleLessonItem } from "@/lib/types/teacher-calendar"

function makeLesson(overrides: Partial<ScheduleLessonItem> = {}): ScheduleLessonItem {
  return {
    id: "lesson-1",
    student_id: "student-1",
    student_name: "Иван Петров",
    topic: "Квадратные уравнения",
    scheduled_at: "2026-04-06T07:00:00Z",
    ends_at: "2026-04-06T08:00:00Z",
    duration_minutes: 60,
    status: "scheduled",
    flags: {
      notification_sent: false,
      confirmed_by_student: false,
      homework_sent: false,
      solution_received: false,
      solution_checked: false,
    },
    ...overrides,
  }
}

describe("LessonCard", () => {
  it("рендерит 5 флагов в неактивном состоянии", () => {
    const lesson = makeLesson()
    render(<LessonCard lesson={lesson} timeLabel="07:00–08:00" />)

    const labels = [
      "Уведомление",
      "Подтверждено",
      "ДЗ отправлено",
      "Решение получено",
      "Проверено",
    ]
    for (const title of labels) {
      const el = screen.getByTitle(title)
      expect(el).toHaveClass("text-muted-foreground")
    }
  })

  it("подсвечивает все флаги при true", () => {
    const lesson = makeLesson({
      flags: {
        notification_sent: true,
        confirmed_by_student: true,
        homework_sent: true,
        solution_received: true,
        solution_checked: true,
      },
    })
    render(<LessonCard lesson={lesson} timeLabel="10:00–11:00" />)

    for (const title of [
      "Уведомление",
      "Подтверждено",
      "ДЗ отправлено",
      "Решение получено",
      "Проверено",
    ]) {
      expect(screen.getByTitle(title)).toHaveClass("text-primary")
    }

    expect(screen.getByText("Иван Петров")).toBeInTheDocument()
    expect(screen.getByText("Квадратные уравнения")).toBeInTheDocument()
    expect(screen.getByText("10:00–11:00")).toBeInTheDocument()
  })

  it("без onOpen не даёт кнопки; с onOpen клик вызывает колбэк", async () => {
    const user = userEvent.setup()
    const onOpen = vi.fn()
    const lesson = makeLesson()

    const { rerender } = render(
      <LessonCard lesson={lesson} timeLabel="07:00–08:00" />,
    )
    expect(document.querySelector("button")).not.toBeInTheDocument()

    rerender(
      <LessonCard lesson={lesson} timeLabel="07:00–08:00" onOpen={onOpen} />,
    )
    await user.click(screen.getByRole("button", { name: /Иван Петров/i }))
    expect(onOpen).toHaveBeenCalledTimes(1)
  })
})
