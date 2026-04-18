/** Сообщения API (часто на английском из backend) → русский для toast. */

const EXACT: Record<string, string> = {
  "Not authenticated": "Требуется вход. Обновите страницу и войдите снова.",
  "Invalid token": "Сессия недействительна. Войдите снова.",
  "User not found": "Пользователь не найден.",
  "Token role mismatch": "Роль в сессии не совпадает с данными. Войдите снова.",
  "Teacher role required": "Нужна роль преподавателя.",
  "Student role required": "Нужна роль ученика.",
  "Request validation failed": "Проверьте введённые данные.",
  "Forbidden": "Доступ запрещён.",
  "Unauthorized": "Требуется вход.",
  "Failed to fetch": "Нет соединения с сервером. Проверьте, что API запущен и адрес в .env.local совпадает с вкладкой (localhost).",
  "Telegram ID already in use": "Этот Telegram ID уже привязан к другому ученику.",
  "Email already in use": "Этот e-mail уже занят.",
}

export function translateApiErrorMessage(message: string): string {
  const t = message.trim()
  if (!t) {
    return "Произошла ошибка"
  }
  if (EXACT[t]) {
    return EXACT[t]
  }
  if (EXACT[message]) {
    return EXACT[message]
  }
  for (const [en, ru] of Object.entries(EXACT)) {
    if (t === en || message.includes(en)) {
      return ru
    }
  }
  return t
}
