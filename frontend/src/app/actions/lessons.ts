"use server"

import { revalidatePath } from "next/cache"

import { serverApiFetch } from "@/lib/api-server"
import { translateApiErrorMessage } from "@/lib/api-error-messages"
import type { LessonFlags } from "@/lib/types/teacher-calendar"

type LessonRead = {
  id: string
  student_id: string
  teacher_id: string
  topic: string
  scheduled_at: string
  duration_minutes: number
  status: string
  notes: string | null
}

function fail(e: unknown): { ok: false; error: string } {
  const raw = e instanceof Error ? e.message : String(e)
  return { ok: false, error: translateApiErrorMessage(raw) }
}

export async function getLessonAction(
  lessonId: string,
): Promise<LessonRead | null> {
  try {
    return await serverApiFetch<LessonRead>(`/v1/lessons/${lessonId}`)
  } catch {
    return null
  }
}

export async function createLessonAction(body: {
  student_id: string
  teacher_id: string
  topic: string
  scheduled_at: string
  status: string
  notes: string | null
  duration_minutes: number
}): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/lessons`, {
      method: "POST",
      body: JSON.stringify(body),
    })
    revalidatePath("/teacher/calendar")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}

export async function updateLessonAction(
  lessonId: string,
  body: {
    student_id: string
    teacher_id: string
    topic: string
    scheduled_at: string
    status: string
    notes: string | null
    duration_minutes: number
  },
): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/lessons/${lessonId}`, {
      method: "PUT",
      body: JSON.stringify(body),
    })
    revalidatePath("/teacher/calendar")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}

export async function deleteLessonAction(
  lessonId: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/lessons/${lessonId}`, { method: "DELETE" })
    revalidatePath("/teacher/calendar")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}

export async function patchLessonFlagsAction(
  lessonId: string,
  patch: Partial<Record<keyof LessonFlags, boolean>>,
): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/lessons/${lessonId}/flags`, {
      method: "PATCH",
      body: JSON.stringify(patch),
    })
    revalidatePath("/teacher/calendar")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}
