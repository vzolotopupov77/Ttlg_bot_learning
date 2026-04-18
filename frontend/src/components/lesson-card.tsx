"use client"

import {
  Bell,
  CheckCircle2,
  Circle,
  FileCheck2,
  Send,
} from "lucide-react"

import { LessonFlagsRow } from "@/components/lesson-flags-row"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { ScheduleLessonItem } from "@/lib/types/teacher-calendar"

type LessonCardProps = {
  lesson: ScheduleLessonItem
  timeLabel: string
  onOpen: () => void
}

export function LessonCard({ lesson, timeLabel, onOpen }: LessonCardProps) {
  return (
    <Card className="gap-0 py-0">
      <CardContent className="space-y-2 p-2">
        <button
          type="button"
          onClick={onOpen}
          className="w-full text-left"
        >
          <p className="font-medium leading-tight">{lesson.student_name}</p>
          <p className="text-muted-foreground text-xs">{timeLabel}</p>
          <p className="mt-1 line-clamp-2 text-xs">{lesson.topic}</p>
        </button>
        <LessonFlagsRow flags={lesson.flags} />
      </CardContent>
    </Card>
  )
}

type LessonLegendProps = {
  className?: string
}

export function LessonFlagsLegend({ className }: LessonLegendProps) {
  const items: { label: string; icon: React.ReactNode }[] = [
    { label: "Уведомление", icon: <Bell className="size-3.5" /> },
    { label: "Подтверждено", icon: <CheckCircle2 className="size-3.5" /> },
    { label: "ДЗ отправлено", icon: <Send className="size-3.5" /> },
    { label: "Решение получено", icon: <Circle className="size-3.5" /> },
    { label: "Проверено", icon: <FileCheck2 className="size-3.5" /> },
  ]
  return (
    <div
      className={cn(
        "text-muted-foreground flex flex-wrap items-center gap-x-4 gap-y-2 text-xs",
        className,
      )}
    >
      {items.map((row) => (
        <span key={row.label} className="inline-flex items-center gap-1.5">
          <span className="text-foreground">{row.icon}</span>
          {row.label}
        </span>
      ))}
    </div>
  )
}

export function AddLessonButton({ onClick }: { onClick: () => void }) {
  return (
    <Button
      type="button"
      variant="outline"
      size="sm"
      className="w-full"
      onClick={onClick}
    >
      + Занятие
    </Button>
  )
}
