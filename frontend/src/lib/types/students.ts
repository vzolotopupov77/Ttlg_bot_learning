import type { LessonFlags } from "@/lib/types/teacher-calendar"

export type StudentListItem = {
  id: string
  name: string
  role: string
  class_label: string | null
  phone: string | null
  email: string | null
  notes: string | null
  /** Telegram user id (число); в API поле `telegram_id`. */
  telegram_id: number | null
  created_at: string
}

export type PaginatedStudents = {
  items: StudentListItem[]
  total: number
  limit: number
  offset: number
}

/** Тело создания/обновления ученика (форма преподавателя). */
export type StudentBody = {
  name: string
  class_label: string | null
  phone: string | null
  email: string | null
  notes: string | null
  telegram_id: number | null
}

export type StudentDetail = StudentListItem

export type StudentLessonItem = {
  id: string
  student_id: string
  teacher_id: string
  topic: string
  scheduled_at: string
  duration_minutes: number
  status: string
  notes: string | null
  flags: LessonFlags
}

export type PaginatedStudentLessons = {
  items: StudentLessonItem[]
  total: number
  limit: number
  offset: number
}

export type StudentStatsRead = {
  student_id: string
  lessons_completed: number
  lessons_total: number
  assignments_done: number
  assignments_total: number
  lessons_solution_checked: number
}

export type DialogueMessage = {
  id: string
  role: "user" | "assistant" | string
  content: string
  created_at: string
}

export type DialogueFeedResponse = {
  items: DialogueMessage[]
  total: number
  limit: number
  offset: number
}
