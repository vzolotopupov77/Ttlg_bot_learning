"use client"

import { useMemo, useState } from "react"

import { BotRequestsFeed } from "@/components/bot-requests-feed"
import { LessonDialog } from "@/components/lesson-dialog"
import { PendingHomework } from "@/components/pending-homework"
import { RescheduleRequests } from "@/components/reschedule-requests"
import { UnconfirmedLessons } from "@/components/unconfirmed-lessons"
import { WeeklySchedule } from "@/components/weekly-schedule"
import type {
  BotRequestItem,
  RescheduleItem,
  ScheduleLessonItem,
  ScheduleResponse,
  StudentListItem,
} from "@/lib/types/teacher-calendar"

type TeacherCalendarViewProps = {
  weekStart: string
  teacherId: string
  initialSchedule: ScheduleResponse
  students: StudentListItem[]
  botRequests: BotRequestItem[]
  unconfirmed: ScheduleLessonItem[]
  pendingHomework: ScheduleLessonItem[]
  rescheduleRequests: RescheduleItem[]
}

export function TeacherCalendarView({
  weekStart,
  teacherId,
  initialSchedule,
  students,
  botRequests,
  unconfirmed,
  pendingHomework,
  rescheduleRequests,
}: TeacherCalendarViewProps) {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [dialogMode, setDialogMode] = useState<"create" | "edit">("create")
  const [dialogLesson, setDialogLesson] = useState<ScheduleLessonItem | null>(
    null,
  )
  const [defaultDayKey, setDefaultDayKey] = useState<string | null>(null)

  /** После refresh расписания подставляем актуальное занятие (флаги и т.д.), иначе в диалоге остаётся старый объект. */
  const lessonForDialog = useMemo(() => {
    if (dialogMode !== "edit" || !dialogLesson) {
      return dialogLesson
    }
    return (
      initialSchedule.items.find((i) => i.id === dialogLesson.id) ?? dialogLesson
    )
  }, [dialogMode, dialogLesson, initialSchedule.items])

  return (
    <div className="space-y-8">
      <WeeklySchedule
        weekStart={weekStart}
        items={initialSchedule.items}
        onOpenLesson={(lesson) => {
          setDialogMode("edit")
          setDialogLesson(lesson)
          setDefaultDayKey(null)
          setDialogOpen(true)
        }}
        onAddLesson={(dayKey) => {
          setDialogMode("create")
          setDialogLesson(null)
          setDefaultDayKey(dayKey)
          setDialogOpen(true)
        }}
      />

      <div className="grid gap-4 md:grid-cols-2">
        <BotRequestsFeed items={botRequests} />
        <RescheduleRequests items={rescheduleRequests} />
        <UnconfirmedLessons items={unconfirmed} />
        <PendingHomework items={pendingHomework} />
      </div>

      <LessonDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        mode={dialogMode}
        lesson={lessonForDialog}
        defaultDayKey={defaultDayKey}
        teacherId={teacherId}
        students={students}
      />
    </div>
  )
}
