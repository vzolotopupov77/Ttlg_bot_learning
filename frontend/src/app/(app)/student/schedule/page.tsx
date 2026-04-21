import { redirect } from "next/navigation"

import { StudentScheduleView } from "@/components/student-schedule-view"
import { fetchStudentSchedule } from "@/lib/api-server"
import { getUser } from "@/lib/auth"
import { parseWeekStart } from "@/lib/calendar-dates"

export default async function StudentSchedulePage({
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
  if (user.role !== "student") {
    redirect("/teacher/calendar")
  }

  const schedule = await fetchStudentSchedule(weekStart)

  return (
    <StudentScheduleView
      weekStart={weekStart}
      studentName={user.name}
      initialSchedule={schedule}
    />
  )
}
