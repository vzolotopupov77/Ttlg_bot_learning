"use client"

import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import type { BotRequestItem } from "@/lib/types/teacher-calendar"

type BotRequestsFeedProps = {
  items: BotRequestItem[]
}

export function BotRequestsFeed({ items }: BotRequestsFeedProps) {
  return (
    <Card className="flex h-full min-h-[200px] flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">Запросы к боту</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden pt-0">
        {items.length === 0 ? (
          <p className="text-muted-foreground text-sm">Нет запросов от учеников</p>
        ) : (
          <ul className="max-h-64 space-y-3 overflow-y-auto pr-1">
            {items.map((row, i) => (
              <li key={row.message_id}>
                {i > 0 ? <Separator className="mb-3" /> : null}
                <p className="font-medium leading-tight">{row.student_name}</p>
                <p className="mt-1 text-sm">{row.text}</p>
                <p className="text-muted-foreground mt-1 text-xs">
                  {format(parseISO(row.created_at), "d MMM yyyy, HH:mm", {
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
