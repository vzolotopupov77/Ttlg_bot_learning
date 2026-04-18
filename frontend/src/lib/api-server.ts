import { cookies } from "next/headers"

import { ACCESS_TOKEN_COOKIE, getApiUrl } from "@/lib/constants"

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
