export type LessonFlags = {
  notification_sent: boolean
  confirmed_by_student: boolean
  homework_sent: boolean
  solution_received: boolean
  solution_checked: boolean
}

export type ScheduleLessonItem = {
  id: string
  student_id: string
  student_name: string
  topic: string
  scheduled_at: string
  ends_at: string
  duration_minutes: number
  status: string
  flags: LessonFlags
}

export type ScheduleResponse = {
  week_start: string
  items: ScheduleLessonItem[]
}

export type BotRequestItem = {
  message_id: string
  dialogue_id: string
  student_id: string
  student_name: string
  text: string
  created_at: string
}

export type BotRequestsResponse = {
  items: BotRequestItem[]
  total: number
  limit: number
  offset: number
}

export type UnconfirmedResponse = {
  items: ScheduleLessonItem[]
  total: number
  limit: number
  offset: number
}

export type RescheduleItem = {
  id: string
  lesson_id: string
  student_id: string
  student_name: string
  proposed_time: string
  requested_at: string
  status: string
}

export type RescheduleListResponse = {
  items: RescheduleItem[]
  total: number
  limit: number
  offset: number
}

export type { PaginatedStudents, StudentListItem } from "@/lib/types/students"

export type RemindResponse = {
  notified_count: number
}
