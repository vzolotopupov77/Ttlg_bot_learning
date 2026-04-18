import { redirect } from "next/navigation"

import { TeacherCalendarView } from "@/components/teacher-calendar-view"
import { getUser } from "@/lib/auth"
import { serverApiFetch } from "@/lib/api-server"
import { parseWeekStart } from "@/lib/calendar-dates"
import type {
  BotRequestsResponse,
  PaginatedStudents,
  RescheduleListResponse,
  ScheduleResponse,
  UnconfirmedResponse,
} from "@/lib/types/teacher-calendar"

export default async function TeacherCalendarPage({
  searchParams,
}: {
  searchParams: Promise<{ week_start?: string }>
}) {
  const sp = await searchParams
  const weekStart = parseWeekStart(sp.week_start)
  const user = await getUser()
  if (!user) {
    redirect("/login")
  }
  if (user.role !== "teacher") {
    redirect("/student/schedule")
  }

  const qs = `week_start=${encodeURIComponent(weekStart)}`
  const [
    schedule,
    students,
    bot,
    unconf,
    pending,
    reschedule,
  ] = await Promise.all([
    serverApiFetch<ScheduleResponse>(`/v1/teacher/schedule?${qs}`),
    serverApiFetch<PaginatedStudents>(`/v1/students?limit=100&offset=0`),
    serverApiFetch<BotRequestsResponse>(
      `/v1/teacher/bot-requests?limit=10&offset=0`,
    ),
    serverApiFetch<UnconfirmedResponse>(
      `/v1/teacher/unconfirmed-lessons?days=2`,
    ),
    serverApiFetch<UnconfirmedResponse>(
      `/v1/teacher/pending-homework?days=2`,
    ),
    serverApiFetch<RescheduleListResponse>(
      `/v1/teacher/reschedule-requests?limit=50&offset=0`,
    ),
  ])

  return (
    <TeacherCalendarView
      weekStart={weekStart}
      teacherId={user.id}
      initialSchedule={schedule}
      students={students.items}
      botRequests={bot.items}
      unconfirmed={unconf.items}
      pendingHomework={pending.items}
      rescheduleRequests={reschedule.items}
    />
  )
}
