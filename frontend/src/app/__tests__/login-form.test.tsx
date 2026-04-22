import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"

const { mockLoginAction } = vi.hoisted(() => ({
  mockLoginAction: vi.fn(),
}))

vi.mock("@/app/actions/auth", () => ({
  loginAction: mockLoginAction,
}))

import { LoginForm } from "@/app/(auth)/login/login-form"

describe("LoginForm (integration)", () => {
  beforeEach(() => {
    mockLoginAction.mockReset()
  })

  it("успешная отправка вызывает loginAction с FormData (email, password, role)", async () => {
    const user = userEvent.setup()
    mockLoginAction.mockResolvedValue(null)

    render(<LoginForm />)
    await user.type(screen.getByLabelText(/E-mail/i), "teacher@example.com")
    await user.type(screen.getByLabelText(/^Пароль$/i), "secret-pass")
    await user.click(screen.getByRole("button", { name: "Войти" }))

    await waitFor(() => expect(mockLoginAction).toHaveBeenCalledTimes(1))
    const formData = mockLoginAction.mock.calls[0][1] as FormData
    expect(formData.get("email")).toBe("teacher@example.com")
    expect(formData.get("password")).toBe("secret-pass")
    expect(formData.get("role")).toBe("teacher")
  })

  it("ошибка от loginAction отображается в Alert", async () => {
    const user = userEvent.setup()
    mockLoginAction.mockResolvedValue({
      error: "Неверный логин или пароль",
    })

    render(<LoginForm />)
    await user.type(screen.getByLabelText(/E-mail/i), "a@b.c")
    await user.type(screen.getByLabelText(/^Пароль$/i), "wrong")
    await user.click(screen.getByRole("button", { name: "Войти" }))

    await waitFor(() =>
      expect(
        screen.getByText("Неверный логин или пароль"),
      ).toBeInTheDocument(),
    )
  })
})
