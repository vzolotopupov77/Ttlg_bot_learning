"use client"

import { format, parseISO } from "date-fns"
import Link from "next/link"

import {
  AddLessonButton,
  LessonCard,
  LessonFlagsLegend,
} from "@/components/lesson-card"
import { buttonVariants } from "@/components/ui/button"
import {
  addWeeksToMonday,
  formatWeekRangeLabel,
  isTodayKey,
  weekDaysFromMonday,
} from "@/lib/calendar-dates"
import type { ScheduleLessonItem } from "@/lib/types/teacher-calendar"
import { cn } from "@/lib/utils"
import { ChevronLeft, ChevronRight } from "lucide-react"

function groupLessonsByDay(
  items: ScheduleLessonItem[],
  weekStart: string,
): Map<string, ScheduleLessonItem[]> {
  const days = weekDaysFromMonday(weekStart)
  const map = new Map<string, ScheduleLessonItem[]>()
  for (const d of days) {
    map.set(d.key, [])
  }
  for (const lesson of items) {
    const key = format(parseISO(lesson.scheduled_at), "yyyy-MM-dd")
    const bucket = map.get(key)
    if (bucket) {
      bucket.push(lesson)
    }
  }
  for (const arr of map.values()) {
    arr.sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at))
  }
  return map
}

function timeRange(lesson: ScheduleLessonItem): string {
  const start = format(parseISO(lesson.scheduled_at), "HH:mm")
  const end = format(parseISO(lesson.ends_at), "HH:mm")
  return `${start}–${end}`
}

type WeeklyScheduleProps = {
  weekStart: string
  items: ScheduleLessonItem[]
  /** Базовый путь для ссылок навигации (например `/teacher/calendar` или `/student/schedule`). */
  basePath?: string
  onOpenLesson?: (lesson: ScheduleLessonItem) => void
  /** Если не передан — кнопка «+ Занятие» скрыта. */
  onAddLesson?: (dayKey: string) => void
}

export function WeeklySchedule({
  weekStart,
  items,
  basePath = "/teacher/calendar",
  onOpenLesson,
  onAddLesson,
}: WeeklyScheduleProps) {
  const days = weekDaysFromMonday(weekStart)
  const byDay = groupLessonsByDay(items, weekStart)
  const prev = addWeeksToMonday(weekStart, -1)
  const next = addWeeksToMonday(weekStart, 1)

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-1">
          <Link
            href={`${basePath}?week_start=${encodeURIComponent(prev)}`}
            aria-label="Предыдущая неделя"
            className={cn(buttonVariants({ variant: "outline", size: "icon-sm" }))}
          >
            <ChevronLeft className="size-4" />
          </Link>
          <Link
            href={basePath}
            className={cn(buttonVariants({ variant: "outline", size: "sm" }))}
          >
            Сегодня
          </Link>
          <Link
            href={`${basePath}?week_start=${encodeURIComponent(next)}`}
            aria-label="Следующая неделя"
            className={cn(buttonVariants({ variant: "outline", size: "icon-sm" }))}
          >
            <ChevronRight className="size-4" />
          </Link>
        </div>
        <p className="text-muted-foreground text-sm font-medium">
          {formatWeekRangeLabel(weekStart)}
        </p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2 md:grid md:grid-cols-7 md:overflow-visible">
        {days.map((day) => {
          const list = byDay.get(day.key) ?? []
          const today = isTodayKey(day.key)
          return (
            <div
              key={day.key}
              className="bg-card flex w-[min(100%,280px)] shrink-0 flex-col gap-2 rounded-lg border p-2 md:min-w-0"
            >
              <div
                className={cn(
                  "rounded-md px-1 py-1 text-center text-sm",
                  today && "ring-2 ring-primary ring-offset-2 ring-offset-background",
                )}
              >
                <div className="text-muted-foreground capitalize">
                  {day.weekdayShort}
                </div>
                <div className="font-semibold">{day.dayNum}</div>
              </div>
              <div className="flex min-h-[120px] flex-1 flex-col gap-2">
                {list.length === 0 ? (
                  <p className="text-muted-foreground flex-1 text-center text-xs">
                    Нет занятий
                  </p>
                ) : (
                  list.map((lesson) => (
                    <LessonCard
                      key={lesson.id}
                      lesson={lesson}
                      timeLabel={timeRange(lesson)}
                      onOpen={
                        onOpenLesson
                          ? () => onOpenLesson(lesson)
                          : undefined
                      }
                    />
                  ))
                )}
                {onAddLesson ? (
                  <AddLessonButton onClick={() => onAddLesson(day.key)} />
                ) : null}
              </div>
            </div>
          )
        })}
      </div>

      <LessonFlagsLegend />
    </div>
  )
}
