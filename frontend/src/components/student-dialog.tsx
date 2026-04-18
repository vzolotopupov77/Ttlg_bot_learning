"use client"

import { useEffect, useState } from "react"
import { Loader2 } from "lucide-react"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  createStudentAction,
  updateStudentAction,
} from "@/app/actions/students"
import type { StudentBody, StudentListItem } from "@/lib/types/students"

function emptyBody(): StudentBody {
  return {
    name: "",
    class_label: null,
    phone: null,
    email: null,
    notes: null,
    telegram_id: null,
  }
}

function studentToBody(s: StudentListItem): StudentBody {
  return {
    name: s.name,
    class_label: s.class_label,
    phone: s.phone,
    email: s.email,
    notes: s.notes,
    telegram_id: s.telegram_id,
  }
}

function normalizeBody(
  name: string,
  classLabel: string,
  phone: string,
  email: string,
  notes: string,
  telegramRaw: string,
): StudentBody | { error: string } {
  const n = name.trim()
  if (!n) {
    return { error: "Укажите ФИО" }
  }
  const em = email.trim()
  if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) {
    return { error: "Некорректный e-mail" }
  }
  const tg = telegramRaw.trim()
  let telegram_id: number | null = null
  if (tg !== "") {
    if (!/^\d+$/.test(tg)) {
      return { error: "Telegram: укажите числовой ID или оставьте пустым" }
    }
    const tidNum = Number(tg)
    if (!Number.isSafeInteger(tidNum) || tidNum < 1) {
      return { error: "Telegram: недопустимое значение" }
    }
    telegram_id = tidNum
  }
  const cl = classLabel.trim()
  const ph = phone.trim()
  const nt = notes.trim()
  return {
    name: n,
    class_label: cl ? cl : null,
    phone: ph ? ph : null,
    email: em ? em : null,
    notes: nt ? nt : null,
    telegram_id,
  }
}

type StudentDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  mode: "create" | "edit"
  student: StudentListItem | null
  onSaved: () => void
}

export function StudentDialog({
  open,
  onOpenChange,
  mode,
  student,
  onSaved,
}: StudentDialogProps) {
  const [name, setName] = useState("")
  const [classLabel, setClassLabel] = useState("")
  const [phone, setPhone] = useState("")
  const [email, setEmail] = useState("")
  const [telegramId, setTelegramId] = useState("")
  const [notes, setNotes] = useState("")
  const [pending, setPending] = useState(false)

  useEffect(() => {
    if (!open) {
      return
    }
    if (mode === "edit" && student) {
      const b = studentToBody(student)
      setName(b.name)
      setClassLabel(b.class_label ?? "")
      setPhone(b.phone ?? "")
      setEmail(b.email ?? "")
      setTelegramId(
        b.telegram_id !== null && b.telegram_id !== undefined
          ? String(b.telegram_id)
          : "",
      )
      setNotes(b.notes ?? "")
    } else {
      const b = emptyBody()
      setName(b.name)
      setClassLabel("")
      setPhone("")
      setEmail("")
      setTelegramId("")
      setNotes("")
    }
  }, [open, mode, student])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const body = normalizeBody(
      name,
      classLabel,
      phone,
      email,
      notes,
      telegramId,
    )
    if ("error" in body) {
      toast.error(body.error)
      return
    }
    setPending(true)
    try {
      if (mode === "create") {
        const res = await createStudentAction(body)
        if (!res.ok) {
          toast.error(res.error)
          return
        }
        toast.success("Ученик добавлен")
      } else if (student) {
        const res = await updateStudentAction(student.id, body)
        if (!res.ok) {
          toast.error(res.error)
          return
        }
        toast.success("Сохранено")
      }
      onOpenChange(false)
      onSaved()
    } finally {
      setPending(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>
              {mode === "create" ? "Добавить ученика" : "Редактировать ученика"}
            </DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="student-name">ФИО</Label>
              <Input
                id="student-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                autoComplete="name"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="grid gap-2">
                <Label htmlFor="student-phone">Телефон</Label>
                <Input
                  id="student-phone"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  autoComplete="tel"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="student-email">E-mail</Label>
                <Input
                  id="student-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                />
              </div>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="student-telegram">Telegram (ID)</Label>
              <Input
                id="student-telegram"
                inputMode="numeric"
                placeholder="Например 123456789"
                value={telegramId}
                onChange={(e) => setTelegramId(e.target.value)}
                autoComplete="off"
              />
              <p className="text-muted-foreground text-xs">
                Числовой идентификатор в Telegram; можно узнать у @userinfobot.
              </p>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="student-class">Класс</Label>
              <Input
                id="student-class"
                value={classLabel}
                onChange={(e) => setClassLabel(e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="student-notes">Заметки</Label>
              <Textarea
                id="student-notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                className="resize-y"
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={pending}
            >
              Отмена
            </Button>
            <Button
              type="submit"
              disabled={pending}
              className="inline-flex items-center gap-2"
            >
              {pending ? (
                <>
                  <Loader2 className="size-4 animate-spin" />
                  Сохранение…
                </>
              ) : (
                "Сохранить"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
