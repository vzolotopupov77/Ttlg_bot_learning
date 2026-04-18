import { Suspense } from "react"

import { StudentsView } from "@/components/students-view"
import { Skeleton } from "@/components/ui/skeleton"
import { serverApiFetch } from "@/lib/api-server"
import type { PaginatedStudents } from "@/lib/types/students"

function StudentsViewFallback() {
  return (
    <div className="flex flex-col gap-4">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-10 w-full max-w-md" />
      <Skeleton className="h-48 w-full" />
    </div>
  )
}

export default async function TeacherStudentsPage() {
  const data = await serverApiFetch<PaginatedStudents>("/v1/students")

  return (
    <Suspense fallback={<StudentsViewFallback />}>
      <StudentsView initialStudents={data.items} total={data.total} />
    </Suspense>
  )
}
