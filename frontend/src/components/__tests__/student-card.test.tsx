import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"

import { StudentCard } from "@/components/student-card"
import type { StudentListItem } from "@/lib/types/students"

function makeStudent(overrides: Partial<StudentListItem> = {}): StudentListItem {
  return {
    id: "s-1",
    name: "Мария Сидорова",
    role: "student",
    class_label: "9А",
    phone: "+7 900 111-22-33",
    email: "maria@example.com",
    notes: "ОГЭ математика",
    telegram_id: 123456789,
    created_at: "2026-01-01T00:00:00Z",
    ...overrides,
  }
}

describe("StudentCard", () => {
  it("отображает основные поля и Telegram ID", () => {
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    render(
      <StudentCard
        student={makeStudent()}
        onEdit={onEdit}
        onDelete={onDelete}
      />,
    )

    expect(screen.getByText("Мария Сидорова")).toBeInTheDocument()
    expect(screen.getByText(/Класс: 9А/)).toBeInTheDocument()
    expect(screen.getByText(/Тел\.: \+7 900 111-22-33/)).toBeInTheDocument()
    expect(screen.getByText("maria@example.com")).toBeInTheDocument()
    expect(screen.getByText(/Telegram ID: 123456789/)).toBeInTheDocument()
    expect(screen.getByText(/ОГЭ математика/)).toBeInTheDocument()
  })

  it("не показывает строку Telegram ID если не привязан", () => {
    render(
      <StudentCard
        student={makeStudent({ telegram_id: null })}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />,
    )
    expect(screen.queryByText(/Telegram ID/)).not.toBeInTheDocument()
  })

  it("показывает плейсхолдер контактов если все пусто", () => {
    render(
      <StudentCard
        student={makeStudent({
          phone: null,
          email: null,
          telegram_id: null,
        })}
        onEdit={vi.fn()}
        onDelete={vi.fn()}
      />,
    )
    expect(screen.getByText("Контакты не указаны")).toBeInTheDocument()
  })

  it("вызывает onEdit и onDelete по кнопкам", async () => {
    const user = userEvent.setup()
    const onEdit = vi.fn()
    const onDelete = vi.fn()
    const student = makeStudent()

    render(
      <StudentCard student={student} onEdit={onEdit} onDelete={onDelete} />,
    )

    await user.click(screen.getByRole("button", { name: "Редактировать" }))
    expect(onEdit).toHaveBeenCalledWith(student)

    await user.click(screen.getByRole("button", { name: "Удалить" }))
    expect(onDelete).toHaveBeenCalledWith(student)
  })
})
