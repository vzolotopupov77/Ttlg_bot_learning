import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"

const setTheme = vi.fn()

const mockUseTheme = vi.hoisted(() =>
  vi.fn(() => ({
    resolvedTheme: "light" as string | undefined,
    setTheme,
    themes: ["light", "dark"],
    theme: "light",
    forcedTheme: undefined,
    systemTheme: undefined,
  })),
)

vi.mock("next-themes", () => ({
  useTheme: () => mockUseTheme(),
}))

import { ThemeToggle } from "@/components/theme-toggle"

describe("ThemeToggle", () => {
  beforeEach(() => {
    setTheme.mockClear()
    mockUseTheme.mockImplementation(() => ({
      resolvedTheme: "light",
      setTheme,
      themes: ["light", "dark"],
      theme: "light",
      forcedTheme: undefined,
      systemTheme: undefined,
    }))
  })

  it("имеет доступную подпись", () => {
    render(<ThemeToggle />)
    expect(
      screen.getByRole("button", { name: "Переключить тему" }),
    ).toBeInTheDocument()
  })

  it("переключает с light на dark", async () => {
    const user = userEvent.setup()
    render(<ThemeToggle />)
    await user.click(screen.getByRole("button", { name: "Переключить тему" }))
    expect(setTheme).toHaveBeenCalledWith("dark")
  })

  it("переключает с dark на light", async () => {
    const user = userEvent.setup()
    mockUseTheme.mockImplementation(() => ({
      resolvedTheme: "dark",
      setTheme,
      themes: ["light", "dark"],
      theme: "dark",
      forcedTheme: undefined,
      systemTheme: undefined,
    }))
    render(<ThemeToggle />)
    await user.click(screen.getByRole("button", { name: "Переключить тему" }))
    expect(setTheme).toHaveBeenCalledWith("light")
  })
})
