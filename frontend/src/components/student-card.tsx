"use client"

import Link from "next/link"
import { Pencil, Trash2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import type { StudentListItem } from "@/lib/types/students"

function initials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return "?"
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

type StudentCardProps = {
  student: StudentListItem
  onEdit: (student: StudentListItem) => void
  onDelete: (student: StudentListItem) => void
}

export function StudentCard({ student, onEdit, onDelete }: StudentCardProps) {
  return (
    <Card className="gap-0 py-0">
      <CardContent className="space-y-3 p-4">
        <div className="flex items-start gap-3">
          <Avatar className="size-11">
            <AvatarFallback>{initials(student.name)}</AvatarFallback>
          </Avatar>
          <div className="min-w-0 flex-1">
            <Link
              href={`/teacher/students/${student.id}`}
              className="font-semibold leading-tight hover:underline"
            >
              {student.name}
            </Link>
            {student.class_label ? (
              <p className="text-muted-foreground text-sm">
                Класс: {student.class_label}
              </p>
            ) : null}
          </div>
          <div className="flex shrink-0 gap-1">
            <Button
              type="button"
              variant="ghost"
              size="icon"
              aria-label="Редактировать"
              onClick={() => onEdit(student)}
            >
              <Pencil className="size-4" />
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="text-destructive hover:text-destructive"
              aria-label="Удалить"
              onClick={() => onDelete(student)}
            >
              <Trash2 className="size-4" />
            </Button>
          </div>
        </div>
        <div className="text-muted-foreground space-y-0.5 text-sm">
          {student.phone ? <p>Тел.: {student.phone}</p> : null}
          {student.email ? <p>{student.email}</p> : null}
          {student.telegram_id != null ? (
            <p>Telegram ID: {student.telegram_id}</p>
          ) : null}
          {!student.phone && !student.email && student.telegram_id == null ? (
            <p className="italic">Контакты не указаны</p>
          ) : null}
        </div>
        {student.notes ? (
          <>
            <Separator />
            <p className="text-muted-foreground line-clamp-4 text-sm whitespace-pre-wrap">
              {student.notes}
            </p>
          </>
        ) : null}
      </CardContent>
    </Card>
  )
}
