"use server"

import { cookies } from "next/headers"
import { redirect } from "next/navigation"

import { ACCESS_TOKEN_COOKIE, getServerApiUrl } from "@/lib/constants"

export type LoginState = { error?: string } | null

function extractTokenFromSetCookie(res: Response): string | null {
  const getSetCookie = res.headers.getSetCookie?.bind(res.headers)
  if (getSetCookie) {
    for (const line of getSetCookie()) {
      if (line.startsWith(`${ACCESS_TOKEN_COOKIE}=`)) {
        return line.split(";")[0].slice(ACCESS_TOKEN_COOKIE.length + 1)
      }
    }
  }
  const combined = res.headers.get("set-cookie")
  if (combined) {
    for (const segment of combined.split(/,(?=\s*[^=]+=)/)) {
      const t = segment.trim()
      if (t.startsWith(`${ACCESS_TOKEN_COOKIE}=`)) {
        return t.split(";")[0].slice(ACCESS_TOKEN_COOKIE.length + 1)
      }
    }
  }
  return null
}

function parseMaxAgeFromSetCookie(res: Response): number | undefined {
  const getSetCookie = res.headers.getSetCookie?.bind(res.headers)
  const lines = getSetCookie ? getSetCookie() : []
  const combined = lines.length ? lines.join(",") : (res.headers.get("set-cookie") ?? "")
  const match = /Max-Age=(\d+)/i.exec(combined)
  if (match) {
    return Number.parseInt(match[1], 10)
  }
  return undefined
}

export async function loginAction(
  _prevState: LoginState,
  formData: FormData,
): Promise<LoginState> {
  const email = String(formData.get("email") ?? "").trim()
  const password = String(formData.get("password") ?? "")
  const role = String(formData.get("role") ?? "")

  if (!email || !password || !role) {
    return { error: "Заполните все поля" }
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { error: "Некорректный формат e-mail" }
  }
  if (role !== "teacher" && role !== "student") {
    return { error: "Выберите роль" }
  }

  const res = await fetch(`${getServerApiUrl()}/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, role }),
  })

  if (!res.ok) {
    return { error: "Неверный логин или пароль" }
  }

  const token = extractTokenFromSetCookie(res)
  if (!token) {
    return { error: "Не удалось получить сессию (нет cookie от сервера)" }
  }

  const maxAge = parseMaxAgeFromSetCookie(res) ?? 60 * 60 * 24

  const cookieStore = await cookies()
  cookieStore.set(ACCESS_TOKEN_COOKIE, token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: process.env.NODE_ENV === "production",
    maxAge,
  })

  redirect(role === "teacher" ? "/teacher/calendar" : "/student/schedule")
}
