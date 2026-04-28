/** Имя cookie с JWT — совпадает с backend (`ttlg_backend.api.deps.ACCESS_TOKEN_COOKIE`). */
export const ACCESS_TOKEN_COOKIE = "ttlg_access_token"

/** URL API для браузера и клиентских компонентов (build-time `NEXT_PUBLIC_*`). */
export function getApiUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"
}

/**
 * URL API для Server Components и server actions внутри контейнера Docker.
 * В compose задайте `API_INTERNAL_URL=http://backend:8000`; иначе — как `getApiUrl()`.
 */
export function getServerApiUrl(): string {
  return process.env.API_INTERNAL_URL ?? getApiUrl()
}
