/** Ответ GET/PUT `/v1/settings` (см. docs/tech/api-contracts.md). */
export type SystemSettings = {
  teacher_name: string
  default_lesson_duration_minutes: number
  lesson_reminder_hours_before: number
  homework_reminder_hours_before: number
}
