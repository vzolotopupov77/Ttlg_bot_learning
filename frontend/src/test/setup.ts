import "@testing-library/jest-dom/vitest"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import { createElement, type ReactNode } from "react"
import { afterAll, afterEach, beforeAll, vi } from "vitest"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"

const defaultSettings = {
  teacher_name: "Тестовый репетитор",
  default_lesson_duration_minutes: 60,
  lesson_reminder_hours_before: 24,
  homework_reminder_hours_before: 48,
}

/** MSW: изоляция интеграционных тестов от реального backend. */
export const mswServer = setupServer(
  http.get(`${API_BASE}/v1/settings`, () =>
    HttpResponse.json(defaultSettings),
  ),
  http.put(`${API_BASE}/v1/settings`, async ({ request }) => {
    const body = (await request.json()) as typeof defaultSettings
    return HttpResponse.json(body)
  }),
  http.post(`${API_BASE}/v1/auth/login`, async () =>
    HttpResponse.json(
      { user: { id: "u1", name: "Test", role: "teacher" } },
      {
        status: 200,
        headers: {
          "Set-Cookie":
            "ttlg_access_token=fake-jwt; Path=/; HttpOnly; Max-Age=3600",
        },
      },
    ),
  ),
)

beforeAll(() => {
  mswServer.listen({ onUnhandledRequest: "warn" })
})

afterEach(() => {
  mswServer.resetHandlers()
})

afterAll(() => {
  mswServer.close()
})

vi.mock("next/link", () => ({
  default: ({
    children,
    href,
    ...props
  }: {
    children: ReactNode
    href: string
    className?: string
  }) => createElement("a", { href, ...props }, children),
}))
