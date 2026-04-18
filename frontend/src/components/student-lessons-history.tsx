import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"

import { LessonFlagsRow } from "@/components/lesson-flags-row"
import { LessonFlagsLegend } from "@/components/lesson-card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { StudentLessonItem } from "@/lib/types/students"

function endsAt(scheduledAt: string, durationMinutes: number): Date {
  const start = parseISO(scheduledAt)
  return new Date(start.getTime() + durationMinutes * 60_000)
}

type StudentLessonsHistoryProps = {
  lessons: StudentLessonItem[]
}

export function StudentLessonsHistory({ lessons }: StudentLessonsHistoryProps) {
  if (lessons.length === 0) {
    return (
      <p className="text-muted-foreground rounded-md border border-dashed p-6 text-center text-sm">
        Пока нет занятий.
      </p>
    )
  }

  return (
    <div className="space-y-3">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Дата</TableHead>
              <TableHead>Время</TableHead>
              <TableHead>Тема</TableHead>
              <TableHead>Статусы</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {lessons.map((lesson) => {
              const start = parseISO(lesson.scheduled_at)
              const end = endsAt(lesson.scheduled_at, lesson.duration_minutes)
              const dateStr = format(start, "d MMM yyyy", { locale: ru })
              const timeStr = `${format(start, "HH:mm")}–${format(end, "HH:mm")}`
              return (
                <TableRow key={lesson.id}>
                  <TableCell className="whitespace-nowrap">{dateStr}</TableCell>
                  <TableCell className="whitespace-nowrap">{timeStr}</TableCell>
                  <TableCell>{lesson.topic}</TableCell>
                  <TableCell>
                    <LessonFlagsRow flags={lesson.flags} />
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </div>
      <LessonFlagsLegend className="pl-1" />
    </div>
  )
}
