"use client"

import { useState } from "react"
import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"

import { LessonFlagsRow } from "@/components/lesson-flags-row"
import { WeeklySchedule } from "@/components/weekly-schedule"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"
import type {
  ScheduleLessonItem,
  ScheduleResponse,
} from "@/lib/types/teacher-calendar"

type StudentScheduleViewProps = {
  weekStart: string
  studentName: string
  initialSchedule: ScheduleResponse
}

function lessonTimeRange(lesson: ScheduleLessonItem): string {
  const start = format(parseISO(lesson.scheduled_at), "HH:mm")
  const end = format(parseISO(lesson.ends_at), "HH:mm")
  return `${start}–${end}`
}

function lessonDateLabel(lesson: ScheduleLessonItem): string {
  return format(parseISO(lesson.scheduled_at), "d MMMM yyyy, EEEE", {
    locale: ru,
  })
}

export function StudentScheduleView({
  weekStart,
  studentName,
  initialSchedule,
}: StudentScheduleViewProps) {
  const [selectedLesson, setSelectedLesson] =
    useState<ScheduleLessonItem | null>(null)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">
        Расписание — {studentName}
      </h1>

      <WeeklySchedule
        weekStart={weekStart}
        items={initialSchedule.items}
        basePath="/student/schedule"
        onOpenLesson={(lesson) => setSelectedLesson(lesson)}
      />

      <Sheet
        open={selectedLesson !== null}
        onOpenChange={(open) => {
          if (!open) {
            setSelectedLesson(null)
          }
        }}
      >
        <SheetContent side="right" className="sm:max-w-md">
          {selectedLesson ? (
            <>
              <SheetHeader>
                <SheetTitle className="pr-8">
                  {selectedLesson.topic || "Занятие"}
                </SheetTitle>
                <SheetDescription className="text-left">
                  <span className="block">{lessonDateLabel(selectedLesson)}</span>
                  <span className="text-foreground mt-1 block font-medium">
                    {lessonTimeRange(selectedLesson)}
                  </span>
                  <span className="text-muted-foreground mt-1 block text-xs">
                    Статус: {selectedLesson.status}
                  </span>
                </SheetDescription>
              </SheetHeader>
              <div className="px-4 pb-4">
                <p className="text-muted-foreground mb-2 text-xs font-medium uppercase">
                  Статусы
                </p>
                <LessonFlagsRow flags={selectedLesson.flags} />
              </div>
            </>
          ) : null}
        </SheetContent>
      </Sheet>
    </div>
  )
}
