"use server"

import { revalidatePath } from "next/cache"

import { serverApiFetch } from "@/lib/api-server"
import { translateApiErrorMessage } from "@/lib/api-error-messages"
import type { StudentBody, StudentDetail } from "@/lib/types/students"

function fail(e: unknown): { ok: false; error: string } {
  const raw = e instanceof Error ? e.message : String(e)
  return { ok: false, error: translateApiErrorMessage(raw) }
}

export async function createStudentAction(
  body: StudentBody,
): Promise<{ ok: true; student: StudentDetail } | { ok: false; error: string }> {
  try {
    const student = await serverApiFetch<StudentDetail>("/v1/students", {
      method: "POST",
      body: JSON.stringify(body),
    })
    revalidatePath("/teacher/students")
    return { ok: true, student }
  } catch (e) {
    return fail(e)
  }
}

export async function updateStudentAction(
  id: string,
  body: StudentBody,
): Promise<{ ok: true; student: StudentDetail } | { ok: false; error: string }> {
  try {
    const student = await serverApiFetch<StudentDetail>(`/v1/students/${id}`, {
      method: "PUT",
      body: JSON.stringify(body),
    })
    revalidatePath("/teacher/students")
    revalidatePath(`/teacher/students/${id}`)
    return { ok: true, student }
  } catch (e) {
    return fail(e)
  }
}

export async function deleteStudentAction(
  id: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/students/${id}`, { method: "DELETE" })
    revalidatePath("/teacher/students")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}
