/** Имя cookie с JWT — совпадает с backend (`ttlg_backend.api.deps.ACCESS_TOKEN_COOKIE`). */
export const ACCESS_TOKEN_COOKIE = "ttlg_access_token"

export function getApiUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"
}
