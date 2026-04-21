import { cookies } from "next/headers"

import { ACCESS_TOKEN_COOKIE, getApiUrl } from "@/lib/constants"
import type { ScheduleResponse } from "@/lib/types/teacher-calendar"
import type { SystemSettings } from "@/lib/types/settings"

export async function serverApiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const cookieStore = await cookies()
  const token = cookieStore.get(ACCESS_TOKEN_COOKIE)?.value
  const url = `${getApiUrl()}${path}`
  const res = await fetch(url, {
    ...init,
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Cookie: `${ACCESS_TOKEN_COOKIE}=${token}` } : {}),
      ...init?.headers,
    },
  })
  if (res.status === 204) {
    return undefined as T
  }
  const json = (await res.json().catch(() => ({}))) as {
    error?: { code?: string; message?: string }
  }
  if (!res.ok) {
    throw new Error(json.error?.message ?? res.statusText)
  }
  return json as T
}

export async function fetchSettings(): Promise<SystemSettings> {
  return serverApiFetch<SystemSettings>("/v1/settings")
}

export async function fetchStudentSchedule(
  weekStart: string,
): Promise<ScheduleResponse> {
  return serverApiFetch<ScheduleResponse>(
    `/v1/student/schedule?week_start=${encodeURIComponent(weekStart)}`,
  )
}
