"use client"

import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { patchRescheduleRequestAction } from "@/app/actions/teacher-dashboard"
import type { RescheduleItem } from "@/lib/types/teacher-calendar"

type RescheduleRequestsProps = {
  items: RescheduleItem[]
}

export function RescheduleRequests({ items: initialItems }: RescheduleRequestsProps) {
  const router = useRouter()
  const [items, setItems] = useState(initialItems)
  const [pendingId, setPendingId] = useState<string | null>(null)

  useEffect(() => {
    setItems(initialItems)
  }, [initialItems])

  const patch = async (id: string, status: "accepted" | "rejected") => {
    const prev = items
    setItems((rows) => rows.filter((r) => r.id !== id))
    setPendingId(id)
    try {
      const res = await patchRescheduleRequestAction(id, status)
      if (!res.ok) {
        setItems(prev)
        toast.error(res.error)
        return
      }
      toast.success(status === "accepted" ? "Перенос принят" : "Перенос отклонён")
      router.refresh()
    } finally {
      setPendingId(null)
    }
  }

  return (
    <Card className="flex h-full min-h-[200px] flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">Запросы на перенос</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden pt-0">
        {items.length === 0 ? (
          <p className="text-muted-foreground text-sm">Нет запросов на перенос</p>
        ) : (
          <ul className="max-h-64 space-y-3 overflow-y-auto pr-1">
            {items.map((row, i) => (
              <li key={row.id}>
                {i > 0 ? <Separator className="mb-3" /> : null}
                <p className="font-medium leading-tight">{row.student_name}</p>
                <p className="text-muted-foreground mt-1 text-xs">
                  Предложено:{" "}
                  {format(parseISO(row.proposed_time), "d MMM yyyy, HH:mm", {
                    locale: ru,
                  })}
                </p>
                <div className="mt-2 flex flex-wrap gap-2">
                  <Button
                    type="button"
                    size="sm"
                    disabled={pendingId === row.id}
                    onClick={() => patch(row.id, "accepted")}
                  >
                    Принять
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant="outline"
                    disabled={pendingId === row.id}
                    onClick={() => patch(row.id, "rejected")}
                  >
                    Отклонить
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}
