import {
  Bell,
  CheckCircle2,
  Circle,
  FileCheck2,
  Send,
} from "lucide-react"

import { cn } from "@/lib/utils"
import type { LessonFlags } from "@/lib/types/teacher-calendar"

function FlagIcon({
  active,
  label,
  children,
}: {
  active: boolean
  label: string
  children: React.ReactNode
}) {
  return (
    <span
      title={label}
      className={cn(
        "inline-flex size-7 items-center justify-center rounded-md border",
        active
          ? "border-primary/40 bg-primary/10 text-primary"
          : "border-border text-muted-foreground",
      )}
    >
      {children}
    </span>
  )
}

export function LessonFlagsRow({ flags }: { flags: LessonFlags }) {
  return (
    <div className="flex flex-wrap gap-1">
      <FlagIcon active={flags.notification_sent} label="Уведомление">
        <Bell className="size-3.5" />
      </FlagIcon>
      <FlagIcon active={flags.confirmed_by_student} label="Подтверждено">
        <CheckCircle2 className="size-3.5" />
      </FlagIcon>
      <FlagIcon active={flags.homework_sent} label="ДЗ отправлено">
        <Send className="size-3.5" />
      </FlagIcon>
      <FlagIcon active={flags.solution_received} label="Решение получено">
        <Circle className="size-3.5" />
      </FlagIcon>
      <FlagIcon active={flags.solution_checked} label="Проверено">
        <FileCheck2 className="size-3.5" />
      </FlagIcon>
    </div>
  )
}
