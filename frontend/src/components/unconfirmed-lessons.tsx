"use client"

import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { remindUnconfirmedAction } from "@/app/actions/teacher-dashboard"
import type { ScheduleLessonItem } from "@/lib/types/teacher-calendar"

type UnconfirmedLessonsProps = {
  items: ScheduleLessonItem[]
}

export function UnconfirmedLessons({ items }: UnconfirmedLessonsProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const remind = async () => {
    setLoading(true)
    try {
      const res = await remindUnconfirmedAction()
      if (!res.ok) {
        toast.error(res.error)
        return
      }
      toast.success(`Напоминания отправлены: ${res.notified_count}`)
      router.refresh()
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="flex h-full min-h-[200px] flex-col">
      <CardHeader className="flex flex-row flex-wrap items-start justify-between gap-2 pb-2">
        <CardTitle className="text-base">Неподтверждённые (2 дня)</CardTitle>
        <Button
          type="button"
          size="sm"
          disabled={items.length === 0 || loading}
          onClick={remind}
        >
          Напомнить всем
        </Button>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden pt-0">
        {items.length === 0 ? (
          <p className="text-muted-foreground text-sm">
            Все занятия подтверждены
          </p>
        ) : (
          <ul className="max-h-64 space-y-2 overflow-y-auto pr-1">
            {items.map((row, i) => (
              <li key={row.id}>
                {i > 0 ? <Separator className="mb-2" /> : null}
                <p className="font-medium leading-tight">{row.student_name}</p>
                <p className="text-muted-foreground text-xs">
                  {format(parseISO(row.scheduled_at), "d MMM yyyy, HH:mm", {
                    locale: ru,
                  })}
                </p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
