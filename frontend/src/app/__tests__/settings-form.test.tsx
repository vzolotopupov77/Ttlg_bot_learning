import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"

const { toastSuccess, toastError } = vi.hoisted(() => ({
  toastSuccess: vi.fn(),
  toastError: vi.fn(),
}))

vi.mock("next/headers", () => ({
  cookies: vi.fn(async () => ({
    get: (name: string) =>
      name === "ttlg_access_token" ? { value: "test-jwt" } : undefined,
  })),
}))

vi.mock("next/cache", () => ({
  revalidatePath: vi.fn(),
}))

vi.mock("sonner", () => ({
  toast: {
    success: toastSuccess,
    error: toastError,
  },
}))

import { SettingsForm } from "@/components/settings-form"

const initialData = {
  teacher_name: "Иван Репетитор",
  default_lesson_duration_minutes: 60,
  lesson_reminder_hours_before: 24,
  homework_reminder_hours_before: 48,
}

describe("SettingsForm (integration + MSW)", () => {
  it("подставляет initialData в поля", () => {
    render(<SettingsForm initialData={initialData} />)
    expect(screen.getByLabelText(/Имя репетитора/i)).toHaveValue("Иван Репетитор")
    expect(
      screen.getByLabelText(/Длительность занятия по умолчанию/i),
    ).toHaveValue(60)
  })

  it("сохранение отправляет PUT на API через server action; toast.success", async () => {
    const user = userEvent.setup()
    toastSuccess.mockClear()

    render(<SettingsForm initialData={initialData} />)

    await user.clear(screen.getByLabelText(/Имя репетитора/i))
    await user.type(screen.getByLabelText(/Имя репетитора/i), "Новое имя")

    await user.click(screen.getByRole("button", { name: "Сохранить" }))

    await waitFor(() =>
      expect(toastSuccess).toHaveBeenCalledWith("Настройки сохранены"),
    )
  })

  it("валидация: пустое имя — ошибка у поля, без успешного toast", async () => {
    const user = userEvent.setup()
    toastSuccess.mockClear()

    render(<SettingsForm initialData={initialData} />)

    await user.clear(screen.getByLabelText(/Имя репетитора/i))
    await user.click(screen.getByRole("button", { name: "Сохранить" }))

    await waitFor(() =>
      expect(screen.getByText("Укажите имя репетитора")).toBeInTheDocument(),
    )
    expect(toastSuccess).not.toHaveBeenCalled()
  })
})
