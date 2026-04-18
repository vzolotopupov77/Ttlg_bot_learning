"use client"

import { useCallback, useState } from "react"
import { usePathname, useRouter, useSearchParams } from "next/navigation"
import { LayoutGrid, Plus, Table2 } from "lucide-react"
import { toast } from "sonner"

import { StudentCard } from "@/components/student-card"
import { StudentDialog } from "@/components/student-dialog"
import { StudentTable } from "@/components/student-table"
import { deleteStudentAction } from "@/app/actions/students"
import { Button } from "@/components/ui/button"
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
import type { StudentListItem } from "@/lib/types/students"

type StudentsViewProps = {
  initialStudents: StudentListItem[]
  total: number
}

export function StudentsView({ initialStudents, total }: StudentsViewProps) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const view =
    searchParams.get("view") === "table" ? "table" : ("cards" as const)

  const setView = useCallback(
    (v: "cards" | "table") => {
      const p = new URLSearchParams(searchParams.toString())
      p.set("view", v)
      router.replace(`${pathname}?${p.toString()}`, { scroll: false })
    },
    [pathname, router, searchParams],
  )

  const refresh = useCallback(() => {
    router.refresh()
  }, [router])

  const [dialogOpen, setDialogOpen] = useState(false)
  const [dialogMode, setDialogMode] = useState<"create" | "edit">("create")
  const [editStudent, setEditStudent] = useState<StudentListItem | null>(null)

  const [deleteTarget, setDeleteTarget] = useState<StudentListItem | null>(null)
  const [deletePending, setDeletePending] = useState(false)

  function openCreate() {
    setDialogMode("create")
    setEditStudent(null)
    setDialogOpen(true)
  }

  function openEdit(s: StudentListItem) {
    setDialogMode("edit")
    setEditStudent(s)
    setDialogOpen(true)
  }

  async function confirmDelete() {
    if (!deleteTarget) {
      return
    }
    setDeletePending(true)
    try {
      const res = await deleteStudentAction(deleteTarget.id)
      if (!res.ok) {
        toast.error(res.error)
        return
      }
      toast.success("Ученик удалён")
      setDeleteTarget(null)
      refresh()
    } finally {
      setDeletePending(false)
    }
  }

  const empty = initialStudents.length === 0

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-muted-foreground text-sm">
          Всего учеников:{" "}
          <span className="text-foreground font-medium">{total}</span>
        </p>
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-lg border border-border p-0.5">
            <Button
              type="button"
              variant={view === "cards" ? "secondary" : "ghost"}
              size="sm"
              className="px-2"
              aria-label="Карточки"
              aria-pressed={view === "cards"}
              onClick={() => setView("cards")}
            >
              <LayoutGrid className="size-4" />
            </Button>
            <Button
              type="button"
              variant={view === "table" ? "secondary" : "ghost"}
              size="sm"
              className="px-2"
              aria-label="Таблица"
              aria-pressed={view === "table"}
              onClick={() => setView("table")}
            >
              <Table2 className="size-4" />
            </Button>
          </div>
          <Button type="button" size="sm" onClick={openCreate}>
            <Plus className="size-4" />
            Добавить
          </Button>
        </div>
      </div>

      {empty ? (
        <p className="text-muted-foreground rounded-lg border border-dashed p-8 text-center text-sm">
          Пока нет учеников. Нажмите «Добавить», чтобы создать первую запись.
        </p>
      ) : view === "cards" ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {initialStudents.map((s) => (
            <StudentCard
              key={s.id}
              student={s}
              onEdit={openEdit}
              onDelete={setDeleteTarget}
            />
          ))}
        </div>
      ) : (
        <StudentTable
          students={initialStudents}
          onEdit={openEdit}
          onDelete={setDeleteTarget}
        />
      )}

      <StudentDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        mode={dialogMode}
        student={editStudent}
        onSaved={refresh}
      />

      <AlertDialog
        open={deleteTarget !== null}
        onOpenChange={(open) => {
          if (!open) {
            setDeleteTarget(null)
          }
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Удалить ученика?</AlertDialogTitle>
            <AlertDialogDescription>
              {deleteTarget
                ? `Запись «${deleteTarget.name}» будет удалена без возможности восстановления из интерфейса.`
                : null}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deletePending}>Отмена</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={(e) => {
                e.preventDefault()
                void confirmDelete()
              }}
              disabled={deletePending}
            >
              Удалить
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
