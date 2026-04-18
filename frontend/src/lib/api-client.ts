import { translateApiErrorMessage } from "@/lib/api-error-messages"
import { getApiUrl } from "@/lib/constants"

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

export async function clientApiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const res = await fetch(`${getApiUrl()}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
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
    const raw = json.error?.message ?? res.statusText
    throw new ApiError(
      res.status,
      json.error?.code ?? "unknown",
      translateApiErrorMessage(raw),
    )
  }
  return json as T
}
