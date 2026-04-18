"use client"

import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"
import { CalendarIcon, Loader2 } from "lucide-react"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Button, buttonVariants } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"
import {
  createLessonAction,
  deleteLessonAction,
  getLessonAction,
  patchLessonFlagsAction,
  updateLessonAction,
} from "@/app/actions/lessons"
import { translateApiErrorMessage } from "@/lib/api-error-messages"
import { cn } from "@/lib/utils"
import type { LessonFlags, ScheduleLessonItem } from "@/lib/types/teacher-calendar"
import type { StudentListItem } from "@/lib/types/students"

function combineDateTimeLocal(date: Date, timeHHMM: string): Date {
  const [h, m] = timeHHMM.split(":").map(Number)
  const out = new Date(date)
  out.setHours(h, m, 0, 0)
  return out
}

function timeToMinutes(t: string): number {
  const [h, m] = t.split(":").map(Number)
  return h * 60 + m
}

const FLAG_LABELS: { key: keyof LessonFlags; label: string }[] = [
  { key: "notification_sent", label: "Уведомление отправлено" },
  { key: "confirmed_by_student", label: "Подтверждено учеником" },
  { key: "homework_sent", label: "ДЗ отправлено" },
  { key: "solution_received", label: "Решение получено" },
  { key: "solution_checked", label: "Решение проверено" },
]

const FLAG_DEFAULTS: LessonFlags = {
  notification_sent: false,
  confirmed_by_student: false,
  homework_sent: false,
  solution_received: false,
  solution_checked: false,
}

type LessonDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  mode: "create" | "edit"
  lesson: ScheduleLessonItem | null
  defaultDayKey: string | null
  teacherId: string
  students: StudentListItem[]
}

export function LessonDialog({
  open,
  onOpenChange,
  mode,
  lesson,
  defaultDayKey,
  teacherId,
  students,
}: LessonDialogProps) {
  const router = useRouter()
  const [date, setDate] = useState<Date>(new Date())
  const [startTime, setStartTime] = useState("10:00")
  const [endTime, setEndTime] = useState("11:00")
  const [studentId, setStudentId] = useState("")
  const [topic, setTopic] = useState("")
  const [notes, setNotes] = useState("")
  /** Оптимистичный слой поверх lesson.flags; сбрасывается при editSyncKey (данные с сервера). */
  const [flagsOverride, setFlagsOverride] = useState<LessonFlags | null>(null)
  const flags: LessonFlags =
    flagsOverride ??
    (mode === "edit" && lesson ? lesson.flags : FLAG_DEFAULTS)
  const [lessonStatus, setLessonStatus] = useState("scheduled")
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState(false)
  const [calOpen, setCalOpen] = useState(false)

  const studentLabel =
    studentId === ""
      ? null
      : (students.find((s) => s.id === studentId)?.name ?? studentId)

  useEffect(() => {
    if (!open || mode !== "create" || !defaultDayKey) {
      return
    }
    setDate(parseISO(`${defaultDayKey}T12:00:00`))
    setStartTime("10:00")
    setEndTime("11:00")
    setStudentId(students[0]?.id ?? "")
    setTopic("")
    setNotes("")
    setLessonStatus("scheduled")
  }, [open, mode, defaultDayKey, students])

  const editSyncKey =
    lesson && mode === "edit"
      ? `${lesson.id}|${lesson.scheduled_at}|${lesson.ends_at}|${lesson.student_id}|${lesson.topic}|${JSON.stringify(lesson.flags)}|${lesson.status}`
      : ""

  useEffect(() => {
    setFlagsOverride(null)
  }, [editSyncKey])

  useEffect(() => {
    if (!open || mode !== "edit" || !lesson) {
      return
    }
    const start = parseISO(lesson.scheduled_at)
    setDate(start)
    setStartTime(format(start, "HH:mm"))
    setEndTime(format(parseISO(lesson.ends_at), "HH:mm"))
    setStudentId(lesson.student_id)
    setTopic(lesson.topic)
    setLessonStatus(lesson.status)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- синхронизация только при изменении данных (editSyncKey), не при новой ссылке lesson
  }, [open, mode, editSyncKey])

  useEffect(() => {
    if (!open || mode !== "edit" || !lesson) {
      return
    }
    let cancelled = false
    void getLessonAction(lesson.id).then((data) => {
      if (!cancelled && data) {
        setNotes(data.notes ?? "")
        setLessonStatus(data.status)
      }
    })
    return () => {
      cancelled = true
    }
  }, [open, mode, lesson?.id])

  const handleSave = async () => {
    const startM = timeToMinutes(startTime)
    const endM = timeToMinutes(endTime)
    if (endM <= startM) {
      toast.error("Время окончания должно быть позже начала")
      return
    }
    if (!studentId || !topic.trim()) {
      toast.error("Заполните ученика и тему")
      return
    }
    const startDt = combineDateTimeLocal(date, startTime)
    const scheduled_iso = startDt.toISOString()
    const duration_minutes = endM - startM

    setSaving(true)
    try {
      if (mode === "create") {
        const res = await createLessonAction({
          student_id: studentId,
          teacher_id: teacherId,
          topic: topic.trim(),
          scheduled_at: scheduled_iso,
          status: "scheduled",
          notes: notes.trim() || null,
          duration_minutes,
        })
        if (!res.ok) {
          toast.error(res.error)
          return
        }
        toast.success("Занятие создано")
      } else if (lesson) {
        const res = await updateLessonAction(lesson.id, {
          student_id: studentId,
          teacher_id: teacherId,
          topic: topic.trim(),
          scheduled_at: scheduled_iso,
          status: lessonStatus,
          notes: notes.trim() || null,
          duration_minutes,
        })
        if (!res.ok) {
          toast.error(res.error)
          return
        }
        toast.success("Занятие сохранено")
      }
      onOpenChange(false)
      router.refresh()
    } catch (e) {
      toast.error(translateApiErrorMessage(e instanceof Error ? e.message : String(e)))
    } finally {
      setSaving(false)
    }
  }

  const patchFlag = async (key: keyof LessonFlags, value: boolean) => {
    if (!lesson || mode !== "edit") {
      return
    }
    setFlagsOverride((prevOv) => ({
      ...lesson.flags,
      ...(prevOv ?? {}),
      [key]: value,
    }))
    const res = await patchLessonFlagsAction(lesson.id, { [key]: value })
    if (!res.ok) {
      setFlagsOverride(null)
      toast.error(res.error)
      return
    }
    router.refresh()
  }

  const handleDelete = async () => {
    if (!lesson) {
      return
    }
    setDeleting(true)
    try {
      const res = await deleteLessonAction(lesson.id)
      if (!res.ok) {
        toast.error(res.error)
        return
      }
      toast.success("Занятие удалено")
      setConfirmDelete(false)
      onOpenChange(false)
      router.refresh()
    } catch (e) {
      toast.error(translateApiErrorMessage(e instanceof Error ? e.message : String(e)))
    } finally {
      setDeleting(false)
    }
  }

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent
          className="gap-4 sm:max-w-lg"
          showCloseButton
        >
          <DialogHeader>
            <DialogTitle>
              {mode === "create" ? "Создать занятие" : "Редактировать занятие"}
            </DialogTitle>
          </DialogHeader>

          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="lesson-student">Ученик</Label>
              <Select
                value={studentId}
                onValueChange={(v) => setStudentId(v ?? "")}
              >
                <SelectTrigger id="lesson-student" className="w-full">
                  <span
                    className={cn(
                      "flex flex-1 truncate text-left",
                      !studentLabel && "text-muted-foreground",
                    )}
                  >
                    {studentLabel ?? "Выберите ученика"}
                  </span>
                </SelectTrigger>
                <SelectContent>
                  {students.map((s) => (
                    <SelectItem key={s.id} value={s.id}>
                      {s.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="grid gap-2">
              <Label>Дата</Label>
              <Popover open={calOpen} onOpenChange={setCalOpen}>
                <PopoverTrigger
                  className={cn(
                    buttonVariants({ variant: "outline" }),
                    "w-full justify-start font-normal",
                    !date && "text-muted-foreground",
                  )}
                >
                  <CalendarIcon className="mr-2 size-4" />
                  {date ? (
                    format(date, "d MMMM yyyy", { locale: ru })
                  ) : (
                    <span>Выберите дату</span>
                  )}
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={(d) => {
                      if (d) {
                        setDate(d)
                        setCalOpen(false)
                      }
                    }}
                    locale={ru}
                    weekStartsOn={1}
                  />
                </PopoverContent>
              </Popover>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="grid gap-2">
                <Label htmlFor="lesson-start">Начало</Label>
                <Input
                  id="lesson-start"
                  type="time"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="lesson-end">Конец</Label>
                <Input
                  id="lesson-end"
                  type="time"
                  value={endTime}
                  onChange={(e) => setEndTime(e.target.value)}
                />
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="lesson-topic">Тема</Label>
              <Input
                id="lesson-topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Тема занятия"
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="lesson-notes">Комментарии / заметки</Label>
              <Textarea
                id="lesson-notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                placeholder="Заметки к занятию"
              />
            </div>

            {mode === "edit" && lesson ? (
              <div className="space-y-3 rounded-lg border p-3">
                <p className="text-sm font-medium">Статусы</p>
                {FLAG_LABELS.map(({ key, label }) => (
                  <div
                    key={key}
                    className="flex items-center justify-between gap-4"
                  >
                    <Label htmlFor={`flag-${key}`} className="font-normal">
                      {label}
                    </Label>
                    <Switch
                      id={`flag-${key}`}
                      checked={flags[key]}
                      onCheckedChange={(v) => patchFlag(key, v)}
                    />
                  </div>
                ))}
              </div>
            ) : null}

            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="secondary" size="sm" disabled>
                Отправить ДЗ
              </Button>
              <Button type="button" variant="secondary" size="sm" disabled>
                Прикрепить файл
              </Button>
              <Button type="button" variant="secondary" size="sm" disabled>
                Напомнить
              </Button>
            </div>
          </div>

          <DialogFooter className="flex-row flex-wrap justify-between gap-2 sm:justify-between">
            {mode === "edit" && lesson ? (
              <Button
                type="button"
                variant="destructive"
                onClick={() => setConfirmDelete(true)}
              >
                Удалить
              </Button>
            ) : (
              <span />
            )}
            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
              >
                Отмена
              </Button>
              <Button type="button" onClick={handleSave} disabled={saving}>
                {saving ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  "Сохранить"
                )}
              </Button>
            </div>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <AlertDialog open={confirmDelete} onOpenChange={setConfirmDelete}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Удалить занятие?</AlertDialogTitle>
            <AlertDialogDescription>
              Это действие нельзя отменить. Занятие будет удалено из расписания.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Отмена</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                "Удалить"
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}
