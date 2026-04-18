"use client"

import Link from "next/link"
import { Pencil, Trash2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { StudentListItem } from "@/lib/types/students"

type StudentTableProps = {
  students: StudentListItem[]
  onEdit: (student: StudentListItem) => void
  onDelete: (student: StudentListItem) => void
}

export function StudentTable({ students, onEdit, onDelete }: StudentTableProps) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ФИО</TableHead>
            <TableHead>Класс</TableHead>
            <TableHead>Телефон</TableHead>
            <TableHead>E-mail</TableHead>
            <TableHead>Telegram</TableHead>
            <TableHead className="text-right">Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {students.map((s) => (
            <TableRow key={s.id}>
              <TableCell className="font-medium">
                <Link
                  href={`/teacher/students/${s.id}`}
                  className="hover:underline"
                >
                  {s.name}
                </Link>
              </TableCell>
              <TableCell>{s.class_label ?? "—"}</TableCell>
              <TableCell>{s.phone ?? "—"}</TableCell>
              <TableCell>{s.email ?? "—"}</TableCell>
              <TableCell>
                {s.telegram_id != null ? String(s.telegram_id) : "—"}
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-1">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    aria-label="Редактировать"
                    onClick={() => onEdit(s)}
                  >
                    <Pencil className="size-4" />
                  </Button>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="text-destructive hover:text-destructive"
                    aria-label="Удалить"
                    onClick={() => onDelete(s)}
                  >
                    <Trash2 className="size-4" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
