import Link from "next/link"
import { notFound, redirect } from "next/navigation"
import { ArrowLeft } from "lucide-react"

import { StudentDialogueFeed } from "@/components/student-dialogue-feed"
import { StudentLessonsHistory } from "@/components/student-lessons-history"
import { StudentStats } from "@/components/student-stats"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { getUser } from "@/lib/auth"
import { serverApiFetch } from "@/lib/api-server"
import type {
  DialogueFeedResponse,
  PaginatedStudentLessons,
  StudentDetail,
  StudentStatsRead,
} from "@/lib/types/students"

export default async function TeacherStudentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const user = await getUser()
  if (!user) {
    redirect("/login")
  }
  if (user.role !== "teacher") {
    redirect("/student/schedule")
  }

  let student: StudentDetail
  let lessons: PaginatedStudentLessons
  let stats: StudentStatsRead
  let dialogue: DialogueFeedResponse

  try {
    ;[student, lessons, stats, dialogue] = await Promise.all([
      serverApiFetch<StudentDetail>(`/v1/students/${id}`),
      serverApiFetch<PaginatedStudentLessons>(
        `/v1/students/${id}/lessons?limit=100&offset=0`,
      ),
      serverApiFetch<StudentStatsRead>(`/v1/students/${id}/stats`),
      serverApiFetch<DialogueFeedResponse>(
        `/v1/students/${id}/dialogue?limit=20&offset=0`,
      ),
    ])
  } catch {
    notFound()
  }

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-8">
      <div>
        <Link
          href="/teacher/students"
          className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm"
        >
          <ArrowLeft className="size-4" />
          Назад к списку
        </Link>
      </div>

      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="text-2xl font-semibold">{student.name}</h2>
          {student.class_label ? (
            <Badge variant="secondary">{student.class_label}</Badge>
          ) : null}
        </div>
        <div className="text-muted-foreground flex flex-wrap gap-x-4 gap-y-1 text-sm">
          {student.phone ? <span>Тел.: {student.phone}</span> : null}
          {student.email ? <span>{student.email}</span> : null}
          {student.telegram_id != null ? (
            <span>Telegram ID: {student.telegram_id}</span>
          ) : null}
        </div>
        {student.notes ? (
          <>
            <Separator className="my-3" />
            <p className="text-muted-foreground whitespace-pre-wrap text-sm">
              {student.notes}
            </p>
          </>
        ) : null}
      </div>

      <section className="space-y-3">
        <h3 className="text-lg font-medium">Статистика</h3>
        <StudentStats stats={stats} />
      </section>

      <section className="space-y-3">
        <h3 className="text-lg font-medium">История занятий</h3>
        <StudentLessonsHistory lessons={lessons.items} />
      </section>

      <section className="space-y-3">
        <StudentDialogueFeed
          studentId={id}
          initialItems={dialogue.items}
          initialTotal={dialogue.total}
        />
      </section>
    </div>
  )
}
